<div align="center">
  
<img src="https://i.imgur.com/kdicZUs.jpg" /></a>

## Description:
### Welcome to HealthHive! This is a social network that focuses on promoting overall health and wellness, such as healthy eating, exercise, and mental health. This could allow users to connect with others who share their interest in living a healthy lifestyle, share tips and advice, and support each other in achieving their goals.

## Technologies Used:
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://GitHub.com/Naereen/StrapDown.js/graphs/commit-activity)
![Maintainer](https://img.shields.io/badge/Maintainer-sally-blue)
![Ask](https://img.shields.io/badge/Ask%20me-anything-1abc9c.svg)

![Django](https://www.djangoproject.com/m/img/badges/djangopowered126x54.gif)

[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)
![CSS](https://img.shields.io/badge/CSS-239120?&style=for-the-badge&logo=css3&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-323330?style=for-the-badge&logo=javascript&logoColor=F7DF1E)
![Bootstrap](https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white)
![Git](https://img.shields.io/badge/GIT-E44C30?style=for-the-badge&logo=git&logoColor=white)
![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)
![Visual Studio Code](https://img.shields.io/badge/Visual_Studio_Code-0078D4?style=for-the-badge&logo=visual%20studio%20code&logoColor=white)
![Heroku badge](https://img.shields.io/badge/Heroku-430098?style=for-the-badge&logo=heroku&logoColor=white)
![Amazon AWS](https://img.shields.io/badge/Amazon_AWS-232F3E?style=for-the-badge&logo=amazon-aws&logoColor=white)
![Material UI](https://img.shields.io/badge/Material%20UI-007FFF?style=for-the-badge&logo=mui&logoColor=white)


## Getting Started

#### [Live Website](https://healthhive.herokuapp.com/)

[Trello](https://trello.com/invite/b/br4FXLB1/ATTI134ec3556bd3adf1fa65e5d94f04fa3e7ADED45F/project-4)

[Wireframe](https://whimsical.com/project-4-2CM5XwL2PLJfumZ8JwXdJB)

[ERD](https://lucid.app/lucidchart/b32445e6-5f6d-43d4-9d86-83365abf2818/edit?viewport_loc=-329%2C151%2C1749%2C1132%2C8xoI5DGM9R4X&invitationId=inv_ea543f2e-a084-4569-8eb6-a0d98118b0b5)

#### NewsFeed Page
<p>
  <strong>"Newsfeed"</strong> is a page where users can stay updated on the latest news and share their own posts. It displays a chronological list of posts with user information, including usernames and profile pictures, along with post titles, content, and posting dates. Users can create posts, like or unlike them, and leave comments to engage in discussions. The NewsFeed aims to foster a community where users can share, interact, and stay informed.
</p>
<img src="https://i.imgur.com/4iVoDdm.png" /></a>

#### Resources Page
<p>Once you log in, there is a <strong>"Resources"</strong> page with a food calorie counter. The <strong>"Food Calorie Counter"</strong> is a user-friendly tool that provides calorie information for various foods, helping users make informed decisions about their food choices and track their calorie intake. It also suggests physical activities required to burn the calories consumed, promoting a balanced approach to managing calorie intake and encouraging an active lifestyle. With its comprehensive features, the Food Calorie Counter empowers users to monitor their calorie intake, make healthier choices, and adopt a more balanced and active lifestyle.
  </p>
<img src="https://i.imgur.com/jkN8zi8.png" /></a>

#### My Profile Page
<p>
  The <strong>"My Profile"</strong> page showcases the user's information, including their profile picture, username, name, email, date of birth, and bio. It also displays the user's posts, with details such as the author, date, title, and content. Users can like/unlike posts, add comments, and view existing comments. The page includes a toggle feature to show/hide the comment form for each post.
</p>
<img src="https://i.imgur.com/ZBYzwzc.png" /></a>

## Interesting Code

The provided code is a Django class-based view called "EditProfile" that allows users to update their profile information, including uploading a profile picture. Here's a simplified explanation:

- The view expects users to be logged in and provides a form for editing the profile.
- When the form is submitted, the code checks if a profile picture was uploaded.
- If a picture is present, it is uploaded to an AWS S3 bucket.
- The URL of the uploaded picture is then saved to the profile instance.
- Finally, the updated profile is saved, and the user is redirected to the profile detail page.

In summary, this code enables users to edit their profiles, including the ability to upload and store profile pictures using AWS S3.

```js
class EditProfile(LoginRequiredMixin, UpdateView):
    model = Profile
    template_name = 'registration/edit_profile.html'
    form_class = EditProfileForm
    success_url = reverse_lazy('profile_detail')

    def form_valid(self, form):
        # Get the profile instance
        profile = form.instance

        # Handle file upload and storage logic here
        profile_pic = self.request.FILES.get('profile_pic', None)
        if profile_pic:
            s3 = boto3.client('s3')
            # Generate a unique key for the file
            key = uuid.uuid4().hex[:6] + profile_pic.name[profile_pic.name.rfind('.'):]
            try:
                bucket = os.environ['S3_BUCKET']
                s3.upload_fileobj(profile_pic, bucket, key)
                # Build the full URL for the uploaded file
                url = f"{os.environ['S3_BASE_URL']}{bucket}/{key}"
                # Assign the URL to the profile_pic field
                profile.profile_pic = url
            except Exception as e:
                print('An error occurred uploading file to AWS S3')
                print(e)

        # Save the profile instance
        return super().form_valid(form)
```

## Next Steps:
- Enhance the post creation process by allowing users to upload images along with their posts. This feature enables users to visually enhance their content and share images related to their posts, providing a more engaging and dynamic experience.

- Implement a user profile search feature that allows users to search for other users' profiles. This feature facilitates easy discovery and connection with other users on the platform, promoting interaction and networking within the community.

- Enrich user profiles by including social media links. Users can provide links to their social media profiles such as Facebook, Twitter, Instagram, or LinkedIn. This addition allows other users to explore and connect with them across different social platforms, expanding their online presence and fostering a sense of community.

- Enable user following functionality to enhance user engagement and connectivity. Users can choose to follow other users, receiving updates on their activities and posts. This feature facilitates networking, collaboration, and the formation of connections within the platform, creating a vibrant and interactive user community.

- Implement a feature to allow users to like comments. By adding a "like" functionality to comments, users can express their appreciation or agreement with specific comments. This feature promotes user engagement and interaction, as well as provides a means for users to acknowledge valuable contributions made by others within the community.