# Restaurant Staff App - Expand Share
A web based application that provides restaurant admins with the tools needed to properly staff their restaurant.
<hr>
<b>Workflow:</b><br>
All the users apply from the same login portal<br>
1. A superuser or application admin can only register <b>Restaurant admin</b> for only one restaurant.<br>
2. A restaurant admin can <i>CRUD</i> locations of the restaurant and <i>CRUD </i> Job Postings. The restaurant admin adds <b>Hiring Manager</b> for each location. <br>
3. The Hiring Manager can view all the job postings belonging to their location and can accept or reject job application and informs the applicant by sending the email.<br>
4. The Applicant/User can view all the jobs posted and can apply to the jobs without logging into the system.
<hr>

<u>To run the application:</ul>

 - `Pip install -r requirements.txt`
 - `python manage.py runserver`
 - Superuser credentials- Username : `superuser@gmail.com`, Password: `passtest`
 -  Create another superuser `python manage.py createsuperuser`
 <hr>
