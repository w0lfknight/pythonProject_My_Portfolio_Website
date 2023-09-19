import os
import smtplib

from flask import Flask, render_template, request
from PIL import Image, ImageDraw, ImageFont
import io
import base64

MY_EMAIL = "ajay20003kumar@gmail.com"
MY_PASSWORD = "sddjrgqklkskdsul"

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get("FLASK_KEY")

@app.route('/', methods=["POST", "GET"])
def index():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        subject = request.form.get("subject")
        message = request.form.get("message")
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(MY_EMAIL, MY_PASSWORD)
            connection.sendmail(
                from_addr=MY_EMAIL,
                to_addrs=MY_EMAIL,

                msg=f"Subject:This is the feed back you got from a user!\n\nHis name is:{name}\n "
                    f"His email is {email}\n"
                    f"His subject is {subject}\n"
                    f"And he wants to say to you that:{message}"
            )


    return render_template('index1.html')


MORSE_CODE_DICT = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.',
    'G': '--.', 'H': '....', 'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..',
    'M': '--', 'N': '-.', 'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.',
    'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-',
    'Y': '-.--', 'Z': '--..',
    '0': '-----', '1': '.----', '2': '..---', '3': '...--', '4': '....-',
    '5': '.....', '6': '-....', '7': '--...', '8': '---..', '9': '----.',
    ' ': ' ',  # Space character
}

def text_to_morse(text):
    morse_code = ""
    for char in text.upper():
        if char in MORSE_CODE_DICT:
            morse_code += MORSE_CODE_DICT[char] + " "
        else:
            morse_code += char  # Keep non-alphanumeric characters as is
    return morse_code.strip()
@app.route('/convert', methods=['POST',"GET"])
def convert():
    input_text = request.form.get('input_text', '')
    morse_result = text_to_morse(input_text)
    return render_template("ttm1.html", morse_result=morse_result), {'morse_result': morse_result}

game_mode = None  # Holds the selected game mode ('pvp' or 'ai')
board = [[' ' for _ in range(3)] for _ in range(3)]
current_player = 'X'
player_names = {'X': 'Player X', 'O': 'Player O'}
message = f"{player_names[current_player]}'s turn."

def check_winner():
    # Check rows
    for row in board:
        if row[0] == row[1] == row[2] and row[0] != ' ':
            return True

    # Check columns
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] and board[0][col] != ' ':
            return True

    # Check diagonals
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] != ' ':
        return True
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] != ' ':
        return True

    return False

def check_draw():
    for row in board:
        for cell in row:
            if cell == ' ':
                # If there is an empty cell, the game is not a draw
                return False

    # If there are no empty cells and no player has won, it's a draw
    if not check_winner():
        return True

    return False

@app.route('/ttc')
def ttc():
    return render_template('tictactoe.html', board=board, message=message)



@app.route('/play', methods=['POST'])
def play():
    global current_player, board, message
    try:
        row = int(request.form['row'])
        col = int(request.form['col'])
    except ValueError:
        message = "Please Enter A Value in Both The Boxes"
    else:
        if board[row][col] == ' ':
            board[row][col] = current_player

            if check_winner():
                message = f"{player_names[current_player]} wins!"
                board = [[' ' for _ in range(3)] for _ in range(3)]
            elif check_draw():
                message = "It's a draw!"
                board = [[' ' for _ in range(3)] for _ in range(3)]
            else:
                current_player = 'X' if current_player == 'O' else 'O'  # Switch players
                message = f"{player_names[current_player]}'s turn."

        else:
            message = "Invalid move. Try again."
    finally:
        return render_template('tictactoe.html', board=board, message=message)

@app.route('/watermark', methods=['GET', 'POST'])
def thumbnail_app():
    watermark_text = None
    text_color = None
    img_str = None

    if request.method == 'POST':
        watermark_text = request.form['watermark_text']
        text_color = request.form['text_color']
        watermark_x = int(request.form['watermark_x'])
        watermark_y = int(request.form['watermark_y'])

        image = Image.open(request.files['image'])
        image.thumbnail((400, 400))

        buffered = io.BytesIO()

        # draw = ImageDraw.Draw(image)
        # font = ImageFont.load_default()
        #
        # draw.text((watermark_x, watermark_y), watermark_text, fill=text_color, font=font)
        image.save(buffered, format="PNG")

        img_str = base64.b64encode(buffered.getvalue()).decode()

    return render_template('watermark.html', watermark_text=watermark_text, text_color=text_color, img_str=img_str)

@app.route('/blogs', methods=["POST", "GET"])
def blog():

    id = request.args.get('id')
    if request.method == 'POST':

        name = request.form.get("username")
        email = request.form.get("email_id")
        website = request.form.get("website")
        message = request.form.get("message")
        if not website:
            website = "not available"
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(MY_EMAIL, MY_PASSWORD)
            connection.sendmail(
                from_addr=MY_EMAIL,
                to_addrs=MY_EMAIL,

                msg=f"Subject:This is the feed back you got from a user!\n\nHis name is:{name}\n "
                    f"His email is {email}\n"
                    f"His website is {website}\n"
                    f"And he wants to say to you that:{message}"
            )


        print(email)
        print(website)
        print(message)
    print(id)

    return render_template("blog-single.html", id=int(id))


@app.route('/really')
def facebook():
    return "<h1>No one uses it anymore</h1>"

@app.route('/cannot_handle')
def instagram():
    return "<h1>Way too much to handle</h1>"

@app.route('/does_not_exist')
def twitter():
    return "<h1>It is ex to everbody now</h1>"

@app.route('/linkedin')
def linkedin():
    return "<h1><a href='https://www.linkedin.com/in/abhay-singh-9072b2158/'>Have It But I do Not Use It Much Sir</a></h1>"



if __name__ == '__main__':
    app.run(debug=True)
