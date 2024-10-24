from flask import Flask, request, render_template, flash
import requests
import praw
from flask_mail import Mail, Message

app = Flask(__name__, template_folder='/Users/dmr/Documents/GitHub/KnowledgeApp/templates')

# Configure Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'dmrathod2018@gmail.com'  # Replace with your email
app.config['MAIL_PASSWORD'] = 'nkva rblx eiic abat'      # Replace with your email password
app.config['MAIL_DEFAULT_SENDER'] = 'dmrathod2018@gmail.com'  # Replace with your email
mail = Mail(app)

# Reddit API credentials
reddit = praw.Reddit(
    client_id='OPa6ofL8Gn3S5z1P7P1Oxw',
    client_secret='82I-JTrRYtk-pXDNglM10X6mWovX7g',
    user_agent='KnowledgeBaseApp'
)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    query = request.form['query']
    
    # Fetch Stack Overflow Results
    stackoverflow_results = fetch_stackoverflow_results(query)
    
    # Fetch Reddit Results
    reddit_results = fetch_reddit_results(query)

    return render_template('results.html', query=query, stackoverflow=stackoverflow_results, reddit=reddit_results)

@app.route('/show_more', methods=['POST'])
def show_more():
    query = request.form['query']
    offset = int(request.form.get('offset', 0))  # Get the current offset

    # Fetch next set of Stack Overflow Results
    stackoverflow_results = fetch_stackoverflow_results(query, offset)

    # Fetch next set of Reddit Results
    reddit_results = fetch_reddit_results(query, offset)

    return render_template('more_results.html', query=query, stackoverflow=stackoverflow_results, reddit=reddit_results, offset=offset + 5)

@app.route('/send_email', methods=['POST'])
def send_email_route():
    query = request.form['query']
    email = request.form['email']

    # Fetch Stack Overflow Results
    stackoverflow_results = fetch_stackoverflow_results(query)
    
    # Fetch Reddit Results
    reddit_results = fetch_reddit_results(query)

    # Send email with results if email is provided
    if email:
        send_email(query, stackoverflow_results, reddit_results, email)
        flash('Email sent successfully!', 'success')
    else:
        flash('Email not provided. Results were not sent.', 'warning')

    return render_template('email_sent.html', email=email)

def fetch_stackoverflow_results(query, offset=0):
    # Stack Overflow API call (limit to 5 results with offset)
    url = f"https://api.stackexchange.com/2.3/search?order=desc&sort=activity&intitle={query}&site=stackoverflow&pagesize=5&page={offset // 5 + 1}"
    response = requests.get(url)
    if response.status_code == 200:
        return [{'title': item['title'], 'link': item['link']} for item in response.json().get('items', [])]
    return []  # Return empty list on failure

def fetch_reddit_results(query, offset=0, limit=5):
    submissions = reddit.subreddit('all').search(query, sort='relevance', limit=None)
    submissions_list = list(submissions)  # Convert to a list

    # Get the required slice based on the offset and limit
    results = [{'title': submission.title, 'permalink': submission.permalink} 
               for submission in submissions_list[offset:offset + limit]]

    return results

def send_email(query, stackoverflow_results, reddit_results, recipient_email):
    msg = Message(f"Search Results for: {query}", recipients=[recipient_email])
    
    # Prepare the email body
    email_body = "Stack Overflow Results:\n"
    
    # Format Stack Overflow results
    for i, result in enumerate(stackoverflow_results, start=1):
        title = result.get('title')  # Assuming each result is a dict with 'title' and 'link'
        link = result.get('link')
        email_body += f"{i}. {title} - {link}\n"

    email_body += "\nReddit Results:\n"
    
    # Format Reddit results
    for i, result in enumerate(reddit_results, start=1):
        title = result.get('title')  # Assuming each result is a dict with 'title'
        link = result.get('permalink')  # Get the correct link for Reddit
        email_body += f"{i}. {title} - https://www.reddit.com{link}\n"  # Construct the full link

    # Set the body of the email
    msg.body = email_body
    
    # Send the email
    try:
        mail.send(msg)
    except Exception as e:
        print(f"Failed to send email: {str(e)}")

if __name__ == '__main__':
    app.run(debug=True)
