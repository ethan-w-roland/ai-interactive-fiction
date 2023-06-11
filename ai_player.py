import argparse
#then the filepath is the path to the game file (default is None)
#then the -d flag turns on debug mode
#then the -m flag sets the model (default is gpt-4)
#then the -l flag sets the output language (default is English)

parser = argparse.ArgumentParser(description='Play an interactive fiction game.')
parser.add_argument('filepath', metavar='filepath', type=str, nargs='?')
parser.add_argument('-d', '--debug', action='store_true', help='turn on debug mode')
parser.add_argument('-m', '--model', type=str, default="gpt-4", help='set the model')
parser.add_argument('-l', '--language', type=str, default="English", help='set the output language')
args = parser.parse_args()

DEBUG = args.debug
MODEL = args.model
LANGUAGE = args.language

print(f"""
Initializing AI-IF interpreter...
  MODEL: {MODEL}
  DEBUG: {DEBUG}
  LANG:  {LANGUAGE}
  FILE:  {args.filepath}
Starting game...\n""")

from loading import loader
loader = loader()

from xyppy.main import make_env, do_step
env = make_env(args.filepath)
game_preamble = do_step(env).strip()

import re, json, openai
openai_creds = json.load(open("openai_creds.json"))
openai.api_key = openai_creds["api_key"]

prompt = open("prompt.txt").read().strip()
prompt += f"\n\n- DISPLAY messages must always be written in {LANGUAGE}, even if you have to translate the original text"

role = "system" if MODEL == "gpt-4" else "user"
messages = [{"role":role,"content":prompt}]
messages += [{"role":"user","content":f"let's begin the game!\nGAME:{game_preamble}"}]

if LANGUAGE == "English":
    # we assume the game itself is written in English...
    print(f"{game_preamble}\n")
    messages += [{"role":"assistant","content":f"THINK: I'll repeat the game text to the user\nDISPLAY: {game_preamble}"}]
    #get user input
    line = input("> ")
    if line == "quit":
        exit()
    messages.append({"role":"user","content":f"USER: {line}"})
    print("")

while True:

    did_submit = False
    while True:

        if not DEBUG:
            loader.start()
        response = openai.ChatCompletion.create(
            model=MODEL,
            messages=messages,
            stop=["GAME:","USER:"]
        )
        response = response["choices"][0]["message"]["content"]
        if DEBUG:
            print(f"*****\n{response.strip()}\n*****")
        else:
            loader.stop()
        messages.append({"role":"assistant","content":response})

        if not response.startswith("THINK:"):
            if DEBUG: print("ERROR: all assistant responses must start with a THINK message")
            messages.append({"role":"user","content":"ERROR: all assistant responses must start with a THINK message"})

        elif "SUBMIT:" in response:
            did_submit = True
            #get game instruction
            command = response.split("SUBMIT:")[1].strip()
            print(f"[{command}]")
            #send instruction to inform
            game_response = do_step(env, command).strip()
            messages.append({"role":"system","content":f"GAME: {game_response}"})
            if DEBUG:
                game_text = " | ".join([re.sub("\s+"," ",line) for line in game_response.split("\n") if line.strip() != ""])
                print(f"<{game_text}>")
    
        elif "DISPLAY:" in response:
            if did_submit: print("")
            output = response.split("DISPLAY:")[1].strip()
            #go to the beginning of the previous line
            print(output + "\n")
            break
    
        else:
            if DEBUG: print("ERROR: all assistant responses must contain either SUBMIT or DISPLAY")
            messages.append({"role":"user","content":"ERROR: all assistant responses must contain either SUBMIT or DISPLAY"})

    #get user input
    line = input("> ")
    if line == "quit":
        break
    messages.append({"role":"user","content":f"USER: {line}"})
    print("")