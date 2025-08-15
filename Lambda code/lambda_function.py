import boto3
import os
import json

# AWS clients
dynamodb = boto3.resource('dynamodb')
kendra = boto3.client('kendra')

# Environment variables (with fallback defaults for local testing)
DYNAMODB_TABLE = os.environ.get('DYNAMODB_TABLE', 'EmployeeData')
KENDRA_INDEX_ID = os.environ.get('KENDRA_INDEX_ID', '')

def lambda_handler(event, context):
    print("Received event:", json.dumps(event, indent=2))

    # Safely extract intent name
    intent_name = (
        event.get('sessionState', {})
             .get('intent', {})
             .get('name', '')
    )

    if intent_name == "GetPTOBalanceIntent":
        return handle_get_pto(event)
    elif intent_name == "GetPolicyIntent":
        return handle_get_policy(event)
    else:
        return close(event, "Sorry, I’m not sure how to handle that yet.")

# ----------------- Handlers -----------------

def handle_get_pto(event):
    slots = (
        event.get('sessionState', {})
             .get('intent', {})
             .get('slots', {}) or {}
    )

    employee_id = (
        slots.get('employeeId', {})
             .get('value', {})
             .get('interpretedValue')
    )

    # Ask for ID if missing
    if not employee_id:
        return elicit_slot(event, 'employeeId',
                           "Could you share your employee ID so I can check your PTO balance?")

    # Fetch from DynamoDB
    table = dynamodb.Table(DYNAMODB_TABLE)
    try:
        resp = table.get_item(Key={'employeeId': employee_id})
    except Exception as e:
        print("DynamoDB error:", e)
        return close(event, "I had trouble reaching the PTO database. Please try again later.")

    # If employee not found, ask again
    if 'Item' not in resp:
        return elicit_slot(event, 'employeeId',
                           f"I couldn't find an employee with ID \"{employee_id}\". "
                           "Please re-enter your employee ID (e.g., emp001).")

    item = resp['Item']
    name = item.get('name', 'Employee')
    pto = item.get('ptoBalance', 0)
    sick = item.get('sickLeaveBalance', 0)

    msg = (f"{name} (ID: {employee_id}), you currently have {pto} PTO day(s) "
           f"and {sick} sick leave day(s) available. "
           "Would you like help applying for leave?")
    return close(event, msg)

def handle_get_policy(event):
    query = event.get('inputTranscript') or ''
    if not query:
        return elicit_intent(event, "What HR policy would you like to know about? For example: maternity leave, WFH, or PTO accrual.")

    if not KENDRA_INDEX_ID:
        return close(event, "Policy search is currently unavailable because the index is not configured.")

    try:
        r = kendra.query(IndexId=KENDRA_INDEX_ID, QueryText=query)
    except Exception as e:
        print("Kendra error:", e)
        return close(event, "I couldn’t access the policy search right now. Please try again shortly.")

    items = r.get('ResultItems') or []
    if not items:
        return close(event, "I couldn't find a relevant policy for that. Could you rephrase or be more specific?")

    excerpt = (items[0].get('DocumentExcerpt') or {}).get('Text') or ''
    return close(event, excerpt[:1000] if excerpt else "I found a relevant document but couldn't extract a snippet.")

# ----------------- Lex V2 Response Helpers -----------------

def elicit_slot(event, slot_to_elicit, message):
    session_state = event.get('sessionState', {}) or {}
    intent = session_state.get('intent', {}) or {}
    intent['state'] = 'InProgress'
    session_state['intent'] = intent

    return {
        "sessionState": {
            **session_state,
            "dialogAction": {"type": "ElicitSlot", "slotToElicit": slot_to_elicit}
        },
        "messages": [{"contentType": "PlainText", "content": message}],
        "sessionId": event.get('sessionId'),
        "requestAttributes": event.get('requestAttributes')
    }

def elicit_intent(event, message):
    session_state = event.get('sessionState', {}) or {}
    intent = session_state.get('intent', {}) or {}
    intent['state'] = 'InProgress'
    session_state['intent'] = intent

    return {
        "sessionState": {
            **session_state,
            "dialogAction": {"type": "ElicitIntent"}
        },
        "messages": [{"contentType": "PlainText", "content": message}],
        "sessionId": event.get('sessionId'),
        "requestAttributes": event.get('requestAttributes')
    }

def close(event, message):
    intent = event.get('sessionState', {}).get('intent', {}) or {}
    return {
        "sessionState": {
            "dialogAction": {"type": "Close"},
            "intent": {
                "name": intent.get('name', 'UnknownIntent'),
                "state": "Fulfilled"
            }
        },
        "messages": [{"contentType": "PlainText", "content": message}],
        "sessionId": event.get('sessionId'),
        "requestAttributes": event.get('requestAttributes')
    }
