from django.core.urlresolvers import reverse
from core.tests.common_test_utils import LoggedInTestCase
from core.models import User


class LoginViewTest(LoggedInTestCase):
    """
    Test case for testing the LoginView
    """
    def setUp(self):
        super(LoginViewTest, self).setUp()

    def test_get_user_login_view(self):
        """
        Test to see we can access the view if not
        logged in.
        """
        response = self.client.get(reverse('login'))
        self.assertEquals(response.status_code, 200)

    def test_get_user_login_view_logged_in_already(self):
        """
        Test to check that if a user is logged in, that they
        are redirected to the dashboard instead of the login.
        """
        self.client.force_login(self.user)
        response = self.client.get(reverse('login'))
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, reverse('dashboard'))

    def test_post_user_login_view_valid_details(self):
        """
        Test to see that we can successfully log into the
        application with correct details.
        """
        data = {'username': 'admin', 'password': 'password'}
        response = self.client.post(reverse('login'), data)
        session = self.client.session
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, reverse('dashboard'))
        self.assertEqual(session["username"], "admin")

    def test_post_user_login_view_invalid_details(self):
        """
        Test to see that if we provide incorrect login detials,
        that we are redirected to the login screen.
        """
        data = {'username': 'admin', 'password': 'badpassword'}
        response = self.client.post(reverse('login'), data)
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, reverse('login'))

    def test_post_user_login_view_blank_details(self):
        """
        Test to see that if we provide blank details
        to the login that we are redirected to login screen.
        """
        data = {'username': '', 'password': ''}
        response = self.client.post(reverse('login'), data)
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, reverse('login'))

    def test_post_user_login_view_logged_in_already(self):
        """
        Test to check that if we are already logged in,
        then we are redirected to the dashboard instead.
        """
        self.client.force_login(self.user)
        data = {'username': 'admin', 'password': 'password'}
        response = self.client.post(reverse('login'), data)
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, reverse('dashboard'))


class LogoutViewTest(LoggedInTestCase):
    """
    Test case for testing the Logout view
    """

    def test_get_user_logout_view(self):
        """
        Test to see that we are redirect correctly,
        when we log out as a user.
        """
        # configure the session
        session = self.client.session
        session['user_pk'] = self.user.id
        session['username'] = self.user.username
        session.save()
        self.client.force_login(self.user)
        response = self.client.get(reverse('logout'))
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, reverse('login'))

    def test_get_user_logout_view_not_logged_in(self):
        """
        Test to check that even if we are not logged in,
        that we are still redirect to the login.
        """
        response = self.client.get(reverse('logout'))
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, reverse('login'))


class UserSettingsViewTest(LoggedInTestCase):
    """
    Test case for UserSettingsView
    """
    def setUp(self):
        super(UserSettingsViewTest, self).setUp()
        session = self.client.session
        # set up the sessions for templates
        session['username'] = self.user.username
        session['user_pk'] = self.user.id
        session.save()

    def test_get_user_settings_view(self):
        """
        Test for getting the view as a valid user
        """
        kwargs = {'slug': "user1"}
        self.client.force_login(self.user)
        response = self.client.get(reverse('user_settings', kwargs=kwargs))
        self.assertEquals(response.status_code, 200)

    def test_get_user_settings_not_logged_in(self):
        """
        Test case for check the user is redirected to the
        login if they are not logged in.
        """
        kwargs = {'slug': "user1"}
        response = self.client.get(reverse('user_settings', kwargs=kwargs))
        self.assertEquals(response.status_code, 302)
        self.assertEqual(response.url,
                         reverse('login') + "?next=/users/profile/user1/")

    def test_get_user_settings_for_other_users(self):
        """
        Test case to check that a user is redirected
        if they try to access another user's inforamtion
        """
        kwargs = {'slug': "admin"}
        self.client.force_login(self.user)
        response = self.client.get(reverse('user_settings', kwargs=kwargs))
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, reverse('dashboard'))


class UserUpdateDetailsViewTest(LoggedInTestCase):
    """
    Test case for the UserUpdateDetailsView
    """
    def setUp(self):
        super(UserUpdateDetailsViewTest, self).setUp()
        session = self.client.session
        # set up the sessions for templates
        session['username'] = self.user.username
        session['user_pk'] = self.user.id
        session.save()

    def test_get_user_update_details(self):
        """
        Test for accessing the view as a standard user
        with correct access rights.
        """
        kwargs = {'slug': "user1"}
        self.client.force_login(self.user)
        response = self.client.get(reverse('user_details', kwargs=kwargs))
        self.assertEquals(response.status_code, 200)

    def test_get_user_update_not_logged_in(self):
        """
        Test to check that the user is directed to the
        login screen if they are not loged in.
        """
        kwargs = {'slug': "user1"}
        next_url = "?next=/users/profile/user1/details/"
        response = self.client.get(reverse('user_details', kwargs=kwargs))
        self.assertEquals(response.status_code, 302)
        self.assertEqual(response.url, reverse('login') + next_url)

    def test_get_user_update_details_for_other_user(self):
        """
        Test to ensure that user cannot access details
        of another user and are redirected.
        """
        kwargs = {'slug': "admin"}
        self.client.force_login(self.user)
        response = self.client.get(reverse('user_details', kwargs=kwargs))
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, reverse('dashboard'))

    def test_valid_post_user_details(self):
        """
        Test view with valid post information
        by changing the first_name of the user.
        """
        data = {
            'username': self.user.username,
            'first_name': "tester",
            'last_name': self.user.last_name,
            'email': self.user.email
        }

        kwargs = {'slug': self.user.username}
        self.client.force_login(self.user)
        response = self.client.post(
            reverse('user_details', kwargs=kwargs), data)
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url,
                          reverse('user_settings', kwargs=kwargs))

        # check that the user was updated
        user = User.objects.get(id=self.user.id)
        self.assertEquals(user.first_name, "tester")

    def test_invalid_post_user_details_not_logged_in(self):
        """
        Test form cannot be updated if the user is
        not logged in.
        """
        data = {
            'username': self.user.username,
            'first_name': "tester",
            'last_name': self.user.last_name,
            'email': self.user.email
        }
        next_url = "?next=/users/profile/user1/details/"
        kwargs = {'slug': self.user.username}
        response = self.client.post(
            reverse('user_details', kwargs=kwargs), data)
        self.assertEquals(response.status_code, 302)
        self.assertEqual(response.url, reverse('login') + next_url)

        # check the user's inforamtion Was not change
        user = User.objects.get(id=self.user.id)
        self.assertEquals(user.first_name, "user")
        self.assertNotEquals(user.first_name, "tester")

    def test_invalid_post_user_details_for_other_user(self):
        """
        Test that a user cannot post inforamtion regarding
        another user and change thier inforamtion
        """
        data = {
            'username': self.user.username,
            'first_name': "tester",
            'last_name': self.user.last_name,
            'email': self.user.email
        }

        kwargs = {'slug': "test"}
        self.client.force_login(self.user)
        response = self.client.post(
            reverse('user_details', kwargs=kwargs), data)
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, reverse('dashboard'))

        # check the user's inforamtion Was not change
        user = User.objects.get(id=self.user.id)
        self.assertEquals(user.first_name, "user")
        self.assertNotEquals(user.first_name, "tester")
