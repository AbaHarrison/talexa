from flask import Flask, render_template_string, request, jsonify
import os

app = Flask(__name__)

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Job Application - HR Analyst</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 700px;
            margin: 0 auto;
        }
        
        .alert {
            background: #fff3cd;
            border: 1px solid #ffc107;
            color: #856404;
            padding: 12px 20px;
            border-radius: 8px;
            margin-bottom: 20px;
            font-size: 14px;
        }
        
        .form-card {
            background: white;
            border-radius: 12px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.1);
            padding: 40px;
            margin-bottom: 20px;
        }
        
        .form-header {
            text-align: center;
            margin-bottom: 30px;
        }
        
        .form-header h1 {
            color: #2d3748;
            font-size: 28px;
            margin-bottom: 8px;
        }
        
        .form-header .job-title {
            color: #667eea;
            font-size: 16px;
            font-weight: 500;
            margin-bottom: 12px;
        }
        
        .form-header .experience {
            color: #718096;
            font-size: 14px;
            margin-bottom: 20px;
        }
        
        .section-title {
            color: #2d3748;
            font-size: 18px;
            font-weight: 600;
            margin: 25px 0 15px;
            padding-bottom: 8px;
            border-bottom: 2px solid #e2e8f0;
        }
        
        .position-summary {
            color: #4a5568;
            font-size: 14px;
            line-height: 1.6;
            margin-bottom: 20px;
            padding: 15px;
            background: #f7fafc;
            border-radius: 6px;
        }
        
        .responsibilities-list {
            list-style: none;
            margin: 15px 0;
            padding: 0;
        }
        
        .responsibilities-list li {
            color: #4a5568;
            font-size: 14px;
            padding: 8px 0;
            padding-left: 20px;
            position: relative;
        }
        
        .responsibilities-list li:before {
            content: "•";
            color: #667eea;
            font-weight: bold;
            position: absolute;
            left: 0;
        }
        
        .form-group {
            margin-bottom: 20px;
        }
        
        label {
            display: block;
            color: #2d3748;
            font-size: 14px;
            font-weight: 500;
            margin-bottom: 8px;
        }
        
        .required {
            color: #e53e3e;
            margin-left: 2px;
        }
        
        input[type="text"],
        input[type="email"],
        select {
            width: 100%;
            padding: 12px 15px;
            border: 2px solid #e2e8f0;
            border-radius: 6px;
            font-size: 14px;
            transition: all 0.3s;
        }
        
        input[type="text"]:focus,
        input[type="email"]:focus,
        select:focus {
            outline: none;
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }
        
        input[type="file"] {
            width: 100%;
            padding: 10px;
            border: 2px dashed #e2e8f0;
            border-radius: 6px;
            cursor: pointer;
            font-size: 14px;
        }
        
        .checkbox-group {
            margin: 15px 0;
        }
        
        .checkbox-item {
            display: flex;
            align-items: flex-start;
            margin: 10px 0;
        }
        
        input[type="checkbox"] {
            margin-right: 10px;
            margin-top: 3px;
            cursor: pointer;
            width: 18px;
            height: 18px;
        }
        
        .checkbox-label {
            font-size: 13px;
            color: #4a5568;
            line-height: 1.5;
            cursor: pointer;
        }
        
        .checkbox-label a {
            color: #667eea;
            text-decoration: none;
        }
        
        .checkbox-label a:hover {
            text-decoration: underline;
        }
        
        .submit-btn {
            width: 100%;
            padding: 14px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 6px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: transform 0.2s, box-shadow 0.2s;
            margin-top: 20px;
        }
        
        .submit-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 20px rgba(102, 126, 234, 0.4);
        }
        
        .submit-btn:active {
            transform: translateY(0);
        }
        
        .success-message {
            background: #d4edda;
            border: 1px solid #c3e6cb;
            color: #155724;
            padding: 15px;
            border-radius: 6px;
            margin-top: 20px;
            display: none;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="alert">
            This is a test version of your form
        </div>
        
        <div class="form-card">
            <div class="form-header">
                <h1>Job Application</h1>
                <div class="job-title">Job Title: HR Analyst (Entry Level)</div>
                <div class="experience">
                    Experience Required: 0-2 years of related experience<br>
                    (Internships Included)
                </div>
            </div>
            
            <div class="section-title">Position Summary</div>
            <div class="position-summary">
                The HR Analyst (Entry Level) provides support in collecting, analyzing, and reporting HR data to improve decision-making and HR processes. This role assists with HR metrics, recruiting analytics, compensation support, workforce planning, and HRIS maintenance. It is ideal for candidates who enjoy working with data and have strong attention to detail.
            </div>
            
            <div class="section-title">Key Responsibilities</div>
            <ul class="responsibilities-list">
                <li>Gather, clean, and analyze HR data from various sources (HRIS, ATS, payroll)</li>
                <li>Prepare weekly, monthly, and quarterly HR reports</li>
                <li>Maintain employee data integrity</li>
                <li>Assist with dashboards and visualizations</li>
                <li>Track recruitment metrics and support the hiring process</li>
                <li>Assist with salary benchmarking and benefits administration</li>
                <li>Participate in HR projects and process improvements</li>
                <li>Support compliance, audits, and documentation</li>
            </ul>
            
            <div class="section-title">Required Qualifications</div>
            <ul class="responsibilities-list">
                <li>Bachelor's degree in HR, Business, or related field</li>
                <li>Knowledge of Power BI, Tableau, or similar tools</li>
            </ul>
            
            <form id="applicationForm" method="POST" enctype="multipart/form-data">
                <div class="section-title">Application Form</div>
                
                <div class="form-group">
                    <label>Name <span class="required">*</span></label>
                    <input type="text" name="name" required>
                </div>
                
                <div class="form-group">
                    <label>Email <span class="required">*</span></label>
                    <input type="email" name="email" required>
                </div>
                
                <div class="form-group">
                    <label>File <span class="required">*</span></label>
                    <input type="file" name="file" accept=".pdf,.doc,.docx" required>
                </div>
                
                <div class="form-group">
                    <label>Location</label>
                    <select name="location">
                        <option value="">Select an option ...</option>
                        <option value="new_york">New York</option>
                        <option value="london">London</option>
                        <option value="berlin">Berlin</option>
                        <option value="tokyo">Tokyo</option>
                        <option value="remote">Remote</option>
                    </select>
                </div>
                
                <div class="checkbox-group">
                    <div class="checkbox-item">
                        <input type="checkbox" id="privacy" name="privacy" required>
                        <label for="privacy" class="checkbox-label">
                            By submitting my application, I confirm that I have read and understood Remotown GMBH's Recruitment Privacy Policy and consent to the processing of my personal data for recruitment purposes, in accordance with applicable data protection laws. <span class="required">*</span>
                        </label>
                    </div>
                </div>
                
                <div class="section-title">Marketing consent</div>
                <div class="checkbox-group">
                    <div class="checkbox-item">
                        <input type="checkbox" id="marketing" name="marketing">
                        <label for="marketing" class="checkbox-label">
                            I would like to receive marketing emails surveys from Remotown
                        </label>
                    </div>
                </div>
                
                <button type="submit" class="submit-btn">Submit Application</button>
                
                <div class="success-message" id="successMessage">
                    Thank you! Your application has been submitted successfully.
                </div>
            </form>
        </div>
    </div>
    
    <script>
        document.getElementById('applicationForm').addEventListener('submit', function(e) {
            e.preventDefault();
            
            const formData = new FormData(this);
            
            fetch('/submit', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Show success message briefly
                    document.getElementById('successMessage').style.display = 'block';
                    
                    // Redirect to the external URL after a short delay
                    setTimeout(() => {
                        window.location.href = data.redirect_url;
                    }, 1500);
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('An error occurred. Please try again.');
            });
        });
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/submit', methods=['POST'])
def submit_application():
    # Get form data
    name = request.form.get('name')
    email = request.form.get('email')
    location = request.form.get('location')
    privacy = request.form.get('privacy')
    marketing = request.form.get('marketing')
    
    # Handle file upload
    file = request.files.get('file')
    if file:
        filename = file.filename
        # In production, save the file securely
        # file.save(os.path.join('uploads', filename))
    
    # Process the application (save to database, send email, etc.)
    print(f"New Application Received:")
    print(f"Name: {name}")
    print(f"Email: {email}")
    print(f"Location: {location}")
    print(f"File: {filename if file else 'No file'}")
    print(f"Privacy Consent: {privacy}")
    print(f"Marketing Consent: {marketing}")
    
    # Return the redirect URL
    return jsonify({
        'success': True, 
        'redirect_url': 'https://nandev-dmazbxa0ggg2ghhr.germanywestcentral-01.azurewebsites.net/form/61dbf474-acd4-4e6a-b432-40cc1807c90c'
    })

if __name__ == '__main__':
    # Create uploads directory if it doesn't exist
    os.makedirs('uploads', exist_ok=True)
    app.run(debug=True, port=5000)