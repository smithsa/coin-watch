from __future__ import print_function
import urllib2
import json



ALEXA_APPLICATION_NAME = "Coin Watch"
API_BASE = "https://min-api.cryptocompare.com"
COIN_REFERENCES_BY_CODE = {
    'ETH': 'Ethereum',
    'ETC': 'Ethereum Classic',
    'BTC': 'Bitcoin',
    'LTC': 'Litecoin',
    'XRP': 'Ripple',
    'BCN': 'ByteCoin',
    'XMR': 'Monero',
    'DODGE': 'Dogecoin',
    'DASH': 'Dash',
    'STR': 'Stellar Lumens',
    'REP': 'Augur',
    'GNT': 'Golem',
    'STEEM' : 'Steem',
    'MAID' : 'MaidSafeCoin',
    'GAME' : 'GameCredits'
}

# --------------- Helpers that build all of the responses ----------------------

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title':  title,
            'content': output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }


# --------------- Functions that control the skill's behavior ------------------

def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """

    session_attributes = {}
    card_title = "Welcome"
    speech_output = "Welcome to "+ALEXA_APPLICATION_NAME+". " \
                    "You can ask me what the price of a coin is. or "\
                    "ask me to give a report. or " \
                    "ask me what are the valid coins."
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "You can ask me what the price of a coin is. For example, " \
                    "What is the price of bitcoin? "\
                    "Or you can ask me to give a report. " \
                    "Or you can ask me what are the valid coins."
                    
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Thank you for trying "+ALEXA_APPLICATION_NAME+". " \
                    "Have a nice day! "
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))

def get_currency_code(currency_name):
    return {
        'ethereum': 'ETH',
        'ethereum classic': 'ETC',
        'bitcoin': 'BTC',
        'litecoin': 'LTC',
        'ripple': 'XRP',
        'bytecoin': 'BCN',
        'monero': 'XMR',
        'dogecoin': 'DOGE',
        'dash': 'DASH',
        'stellar lumens': 'STR',
        'augur': 'REP',
        'golem': 'GNT',
        'steem' : 'STEEM',
        'maidsafecoin' : 'MAID',
        'gamecredits' : 'GAME'
    }.get(currency_name, "unkn")
    
def get_coin_prices(intent, session):
    session_attributes = {}
    reprompt_text = None
    should_end_session = True
    card_title = "Coin Report"
    if 'ReportLanguage' in intent['slots']:
        reportLan = intent['slots']['ReportLanguage']['value']
        if(reportLan in ['report', 'a report', 'coin report', 'a coin report', 'coin prices']):
            response = urllib2.urlopen(API_BASE + "/data/pricemulti?fsyms=BTC,ETH,LTC,XRP&tsyms=USD")
            prices = json.load(response)
            response_str = ""
            count = 0
            for price in prices:
                currency = price
                price_point = prices[price]['USD']
                if(count == 0):
                    response_str += COIN_REFERENCES_BY_CODE[str(currency)] +" is $"+str(price_point)
                elif(count == len(prices)-1):
                    response_str += ", and "+COIN_REFERENCES_BY_CODE[str(currency)] +" is $"+str(price_point)
                else:   
                    response_str += ", "+COIN_REFERENCES_BY_CODE[str(currency)] +" is $"+str(price_point)
                
                response_str = response_str.capitalize()
                count = count + 1
        
            speech_output = response_str
        else:
            speech_output = "I'm not sure what you are asking for. " \
                            "Please try again or ask for help."
            should_end_session = False      
    else:
        speech_output = "I'm not sure what you are asking for. " \
                        "Please try again or ask for help."
        should_end_session = False  
        
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def get_valid_coins(intent, session):
    session_attributes = {}
    reprompt_text = "None"
    should_end_session = True
    card_title = "Valid Coins"
    if 'ValidLanguage' in intent['slots']:
        validLan = intent['slots']['ValidLanguage']['value']
        if(validLan in ['valid coins','coin','coins']):
            response_str = ""
            coins = ['GameGredits','Ethereum', 'Ethereum Classic','Bitcoin','Litecoin','Ripple','Bytecoin','Monero','Dogecoin','Dash','Stellar Lumens','Augur','Golem','Steem','MaidSafeCoin']
            response_str = "The possible valid cryptocurrencies are "
            coins.sort()
            coin_coint = 0
            for coin in coins:   
                if(coin_coint == 0):
                    response_str += coin
                elif(coin_coint == len(coins)-1):
                    response_str += ", and "+coin
                else:
                    response_str += ", "+coin
                coin_coint = coin_coint + 1    
        
            speech_output = response_str  
        else:
            speech_output = "I'm not sure what you are asking for. " \
                            "Please try again or ask for help."
            should_end_session = False      
    else:
        speech_output = "I'm not sure what you are asking for. " \
                        "Please try again or ask for help."
        should_end_session = False  
        
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def get_specific_coin_prices(intent, session):
    session_attributes = {}
    card_title = "Coin Price"
    speech_output = "I'm not sure which cryptocurrency coin you are referring to. " \
                    "Please try again."
    reprompt_text = "I'm not sure which cryptocurrency coin you are referring to. " \
                    "Ask "+ALEXA_APPLICATION_NAME+", what are the valid coins?."
    should_end_session = False

    if 'CryptoPrice' in intent['slots']:
        currency = intent['slots']['CryptoPrice']['value']
        currency_code = get_currency_code(currency)
        if(currency_code != "unkn"):
            response = urllib2.urlopen(API_BASE + "/data/price?fsym="+currency_code+"&tsyms=USD")
            price = json.load(response)
            speech_output = currency.capitalize() +" is $"+str(price['USD'])
            should_end_session = True
        else:
            speech_output = "I'm not sure what the price of this coin is. " \
                        "Please try again."
            
    else:
        speech_output = "I'm not sure what your what the price of this coin is. " \
                        "Please try again."
        reprompt_text = "I'm not sure what the price of this coin is. " \
                        "You can ask, for example, what is the price of Bitcoin?. "\
                        "Please try again."
       
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))  

def get_help_response(intent, session):
    session_attributes = {}
    card_title = "Help"
    speech_output = "Here are some things you can say: "\
                    "What is the price of Bitcoin? " \
                    "Give me a report. "\
                    "What are the valid cryptocurrencies? "\
                    "You can also say, stop, if you're done. "\
                    "So, how can I help?"
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "Here are some things you can say: " \
                    "To get the price of a coin, ask, what is the price of Bitcoin? "\
                    "Or to get a report of popular coins: say, give me a report. " \
                    "Or to get valid coins supported by Coin Watch: ask, what are the valid coins? " \
                    "How can I help?"
                    
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

# --------------- Events ------------------

def on_session_started(session_started_request, session):
    """ Called when the session starts """

    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return get_welcome_response()


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers,
    if intent_name == "GetSpecificPrice":
        return get_specific_coin_prices(intent, session)
    elif intent_name == "GetCoinPrices":
        return get_coin_prices(intent, session)
    elif intent_name == "GetValidCurrencies":
        return get_valid_coins(intent, session)
    elif intent_name == "AMAZON.HelpIntent" or intent_name == "IntentNotKnown":
        return get_help_response(intent, session)
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent" or intent_name == "EndSesssion":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here


# --------------- Main handler ------------------

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """
    # if (event['session']['application']['applicationId'] !=
    #         "amzn1.echo-sdk-ams.app.[unique-value-here]"):
    #     raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])
