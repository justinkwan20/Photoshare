# Photoshare
Flask Based web application that I built for my CS 460 class on databases. I used mysql database to store the data locally and used flask web framework in order to create the web application.

# <span class="s1">**CS460/660 Project Assignment 1**</span>

<span class="s1">**PhotoShare: An on-line photo social network system**</span>

## <span class="s1">**Purpose of the project**</span>

<span class="s1">In this project, you will design, implement and document a database system for a web based photo social sharing application. You need also to provide the web based interface to the database. The final system should be functional and will be similar to Flickr!</span>


## <span class="s1">**Data**</span>

<span class="s1">The system should manage the following information:</span>

<span class="s1">Users<span class="Apple-converted-space"></span></span>

<span class="s1">Each user is identified by a unique user id and has the following attributes: first name, last name, email, date of birth, hometown, gender, and password. A user can have a number of Albums.</span>

<span class="s1">Friends</span>

<span class="s1">Each user can have any number of friends.<span class="Apple-converted-space"></span></span>

<span class="s1">Albums<span class="Apple-converted-space"></span></span>

<span class="s1">Each album is identified by a unique album id and has the following attributes: name, owner (user) id, and date of creation. Each album can contain a number of photos.<span class="Apple-converted-space"></span></span>

<span class="s1">Photos<span class="Apple-converted-space"></span></span>

<span class="s1">Each photo is identified by a unique photo id and must belong to an album. Each photo has the following attributes: caption and data. The 'data' field should contain the actual binary representation of the uploaded image file. Alternatively, the 'data' field can store the file location of the file that stores the image. Each photo can only be stored in one album and is associated with zero, one, or more tags.<span class="Apple-converted-space"></span></span>

<span class="s1">Tags<span class="Apple-converted-space"></span></span>

<span class="s1">Each tag is described by a single word. Many photos can be tagged with the same tag. For the purpose of this project we will assume that all tags are lower-cased and contain no spaces. For example, you can have many photos tagged with the tag "boston" in different albums.</span>

<span class="s1">Comments<span class="Apple-converted-space"></span></span>

<span class="s1">Each comment is identified by a unique comment id and has the following attributes: text (i.e., the actual comment), the comment's owner (a user) and the date the comment was left.<span class="Apple-converted-space"></span></span>

## <span class="s1">**Use cases**</span>

<span class="s1">The following interaction with the system should be implemented.<span class="Apple-converted-space"></span></span>

### <span class="s1">**User management**</span>

<span class="s2">**Becoming a registered user.**</span> <span class="s1">Before being able to upload photos a user should register by providing their first name, last name, email address, date of birth, and a password. If the user already exists in the database with the same email address an error message should be produced. The other additional information about each user is optional.</span>

<span class="s2">**Adding and Listing Friends.** </span><span class="s1">You should allow a user to add a new friend on the friend list. For simplicity, you do not have to verify the friendship relationship. Also, you should allow the user to search for other users in the system (in order to find friends to add.) Finally, you must allow a user to list his/her friends.</span>

<span class="s2">**User activity.**</span> <span class="s1">To motivate users in using the site we'd like to identify the ones who make the largest contribution and list them on the site. We'll measure the contribution of a user as the number of photos they have uploaded plus the number of comments they have left for photos belonging to other users. The top 10 users should be reported.<span class="Apple-converted-space"></span></span>

### <span class="s1">**Album and photo management**</span>

<span class="s2">**Photo and album browsing.**</span> <span class="s1">Every visitor to the site, registered or not, should be allowed to browse photos. In this project we will assume that all photos and albums are made public by their authors.<span class="Apple-converted-space"></span></span>

<span class="s2">**Photo and album creating.**</span> <span class="s1">After registration, users can start creating albums and uploading photos. The relevant fields are described above. Users should also be able to delete both albums and photos. If an non-empty album is deleted its photos should also be purged. Users should only be allowed to modify and delete albums and photos which they own.<span class="Apple-converted-space"></span></span>

### <span class="s1">**Tag management**</span>

<span class="s2">**Viewing your photos by tag name.**</span> <span class="s1">Tags provide a way to categorize photos and each photo can have any number of tags. You may think of them as virtual albums. For example, suppose that a user has two distinct albums each of which contains a photo with the tag 'friends'. The means should be provided to view the virtual album created if we select all the photos owned by the user that contain the tag 'friends'. One possible user interface design for this functionality is to present tags as hyperlinks. When a tag is clicked the photos tagged with it are listed.<span class="Apple-converted-space"></span></span>

<span class="s2">**Viewing all photos by tag name.**</span> <span class="s1">Furthermore, the system should allow users to view all photos that contain a certain tag, i.e., not only the ones they have uploaded but also photos that belong to other users. This functionality is similar to the one above and hence they could be presented together. One possible representation is a switch of the form "View all photos / View my photos" that when toggled switches from one view to the other.<span class="Apple-converted-space"></span></span>

<span class="s2">**Viewing the most popular tags.**</span> <span class="s1">A function should be provided that lists the most popular tags, i.e., the tags that are associated with the most photos. Again, tags should be clickable so that when a user clicks one of them all photos tagged with this tag are listed.<span class="Apple-converted-space"></span></span>

<span class="s2">**Photo search.**</span> <span class="s1">The functionality should be provided so that both visitors and registered users can search through the photos by specifying conjunctive tag queries. For example a visitor could enter the words "friends boston" in a text field, click the search button and be presented with all photos that contain both the tag "friends" and the tag "boston".<span class="Apple-converted-space"></span></span>

### <span class="s1">**Comments**</span>

<span class="s2">**Leaving comments.**</span> <span class="s1">Both registered and anonymous users can leave comments. Users cannot leave comments for their own photos. If registered user leaves a comment then this counts towards their contribution score as described above.<span class="Apple-converted-space"></span></span>

<span class="s2">**Like functionality.**</span> <span class="s1">We want to add a **Like** functionality. If a user likes a photo, should be able to add a like to the photo. Also, we must be able to see how many likes a photo has and the users that liked this photo.<span class="Apple-converted-space"></span></span>

<span class="s3">**Search on comments.** </span><span class="s1">In this feature, you want to implement a search function based on the comments. The user can specify a text query (one or more words) and the system should find the users that have created comments <span class="Apple-converted-space"></span>that exactly match the query text. The system should return these users ordered by the number of comments that match the query for each such user in descending order.</span><span class="s3"><span class="Apple-converted-space"></span></span>

### <span class="s1">**Recommendations**</span>

<span class="s2">**Friend recommendation.** </span><span class="s1">We want to recommend possible **new** friends to a user. One simple approach to recommend new friends to a user A is to find all friends of A and find their common friends. That approach is called “friend-of-friends” and is used in some systems as a first step to make friend recommendation. <span class="Apple-converted-space"></span>Order the recommendations based on how many times each reccomended friend appears in the lists of friends of friends.<span class="Apple-converted-space"></span></span>

<span class="s2">**'You-may-also-like' functionality.**</span> <span class="s1">Given the type of photos uploaded by a user we'd like to make some recommendations to them about other photos they may like. To achieve that do the following: Take the five most commonly used tags among the user's photos. Perform a disjunctive search through all the photos for these five tags. A photo that contains all five tags should be ranked higher than one that contained four of the tags and so on. Between two photos that contain the same number of matched tags prefer the one that is more concise, i.e., the one that has fewer tags over all.<span class="Apple-converted-space"></span></span>

## <span class="s1">**Rules of the Project**</span>

### <span class="s1">**Implementation Tools**</span>

<span class="s1">We will provide you with all the tools you need to complete this project. All queries to the database will be made via SQL statements. For this project, you are expected to be familiar with Python and SQL. Everything else will be explained or automated for you. The project is to be done in groups of two. You are allowed to talk with each other about the project but you are not allowed to share code or queries. If you have questions about the project you should ask the Instructor first.</span>

## <span class="s1">**Overview of Project Phases**</span>

<span class="s1">You will be provided with the infrastructure for this project, and only asked to fill in a few pieces. We have divided the project into 3 phases. You will be given detailed instructions and examples of all the utilities required for each phase.  However, you need to submit everything together after completing all the phases.<span class="Apple-converted-space"></span></span>

### <span class="s1">**Phase I - Design**</span>

<span class="s1">Initially, you must design and create a database for the application. This includes creating tables to store this data, and designing rules for how these tables relate to each other so that the data they store can be combined in meaningful ways. As part of the report for this phase, you will turn in an E-R diagram of your database design, and the translation to the relational schema. Also, you have to provide all the constraints and the SQL code that you used to enforce them (CHECK or ASSERTION clauses).<span class="Apple-converted-space"></span></span>

### <span class="s1">**Phase II - API Implementation**</span>

<span class="s1">In this phase, you should write the SQL queries and some Python code that implements an interface to your database and executes the queries. This part will be used in the next phase for the web interface.<span class="Apple-converted-space"></span></span>

### <span class="s1">**Phase III - Web Site Extension**</span>

<span class="s1">Finally, you will create a web site for your database and add the photo sharing functionality.<span class="Apple-converted-space"></span></span>

## <span class="s1">**Deliverable**</span>

<span class="s1">You should provide two deliverables for this project. The first one is the database design and the second is the final system.</span>

<span class="s1">Here are more details:</span>

*   <span class="s4"></span><span class="s1">Friday, October <span class="Apple-converted-space"></span>6, at 5PM: You need to provide a report with the E/R diagram, the relational schema, the assumptions that you make, and the integrity constraints. You can submit the report either using gsubmit (to cs460/cs660) or handing in a hard copy report in the CS 460 drop box.  
    </span>
*   <span class="s4"></span><span class="s1">Thursday, October 26, at 11:59PM. The final report with the code and the additional assumptions that you made and the limitations of your system. In particular, you should submit using gsubmt the following:<span class="Apple-converted-space"></span></span>

1.  <span class="s4"></span><span class="s1">The final report that should contain the final schema and any additional assumptions and constraints you made.<span class="Apple-converted-space"></span></span>
2.  <span class="s4"></span><span class="s1">A zip file with the photoshare directory (all your code). Alternatively, you can gsubmit the photoshare directory.  
    </span>

<span class="s1">  
</span>
