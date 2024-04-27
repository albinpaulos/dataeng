import csv
import boto3
from botocore.exceptions import NoCredentialsError
from datetime import datetime
import os
from flask import Flask, request
def extract_values_from_csv(csv_file):
    first_names = []
    emails = []
    with open(csv_file, 'r', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            first_names.append(row['first_name'])
            emails.append(row['email'])
    return first_names, emails

def save_to_csv(first_names, emails, output_file):
    with open(output_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['first_name', 'email'])
        for first_name, email in zip(first_names, emails):
            writer.writerow([first_name, email])

def check_file_in_s3(bucket_name, file_key):
    s3 = boto3.client('s3')
    try:
        s3.head_object(Bucket=bucket_name, Key=file_key)
        return True
    except Exception as e:
        return False

def process_csv_from_s3(event, output_bucket):
    input_bucket = event['Records'][0]['s3']['bucket']['name']
    input_file_key = event['Records'][0]['s3']['object']['key']
    input_file_name = os.path.splitext(os.path.basename(input_file_key))[0]
    s3 = boto3.client('s3')
    try:
        local_input_file = '/tmp/input.csv'
        s3.download_file(input_bucket, input_file_key, local_input_file)
        first_names, emails = extract_values_from_csv(local_input_file)
        
        # Generate output file name  with timestamp
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        output_file = f'output_{input_file_name}_{timestamp}.csv'
        
        local_output_file = f'/tmp/{output_file}'
        save_to_csv(first_names, emails, local_output_file)
        s3.upload_file(local_output_file, output_bucket, output_file)
        print("Results saved to S3 bucket:", output_bucket, "as", output_file)
        
        # Remove the source file from input  bucket
        s3.delete_object(Bucket=input_bucket, Key=input_file_key)
        print("Source file removed from input bucket:", input_file_key)
        
        # Remove the source file from /tmp directory
        os.remove(local_input_file)
        print("Source file removed from /tmp directory.")
    except NoCredentialsError:
        print("Credentials not available.")
        
def lambda_handler(event, context):
    output_bucket = 'destdata-47'

    if 'Records' in event and len(event['Records']) > 0:
        process_csv_from_s3(event, output_bucket)
    else:
        print("No valid S3 event found in the input.")

#######################################################################################

def get_secret_key():
    return 'my_secret_key'  # Poor coding: Hardcoded secret

@app.route('/')
def index():
    # Vulnerable code: Poor input validation
    name = request.args.get('name')
    
    # Vulnerable code: SQL injection vulnerability
    db = pymysql.connect(host="localhost", user="root", password="password", database="users")
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users WHERE name='%s'" % name)
    user = cursor.fetchone()
    db.close()
    
    # Vulnerable code: Unsanitized output
    return "Hello, " + name

@app.route('/vulnerable')
def vulnerable():
    # Vulnerable code: Insecure direct object reference
    file_path = request.args.get('file')
    # Vulnerable code: Directory traversal vulnerability
    with open(file_path, 'r') as file:
        data = file.read()
    return data

if __name__ == '__main__':
    # Poor coding: No proper error handling
    try:
        app.run(debug=True)
    except Exception as e:
        print("Error:", e)
        sys.exit(1)
