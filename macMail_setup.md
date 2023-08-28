## Setting up macOS Mail Client for Local SMTP Server

### Prerequisites
- Make sure email_followup_server.py script is running.

### 1. Open Mail Accounts
- Open the Mail application.
- From the menu bar, select `Mail` > `Accounts`.

### 2. Add a New Account
- Click the `Add Account...` button to add a new account.
- From the list of mail account providers, choose `Add Other Account...` and click `@ Mail Account`.

### 3. Enter Account Details
- **Full Name**: Enter your name.
- **Email Address**: Enter the email address you want to use with this local server (it doesn't have to be a real email address), e.g. [name]@localhost
- **Password**: Enter any password (since the local SMTP server is set to accept any login).
- Click `Sign In`.

### 4. Configure Server Settings
Since the Mail app will not be able to verify the account, it'll show an error and provide you with fields to manually enter server details.
- **Account Type**: Choose `POP`.
- **Incoming Mail Server**: Enter `127.0.0.1`.
- **Outgoing Mail Server**: Enter `127.0.0.1`.
- Click `Sign In`.
- Click `Next`.
- Close the `Preferences` window.

### 5. Configure Outgoing Mail Server (SMTP)
- From the menu bar, select `Mail` > `Settings`.
- Under the `Accounts` tab, select the new server and find the `Outgoing Mail Server (SMTP)` section under the `Server Settings`.
- Untick `Automatically manage connection settings`.
- in the `Port` field, Enter `8025`.
- Click `Save`.

### 6. Finish Setup
- Close the `Preferences` window.
- When prompted, save any changes you made.

### 7. Test the Setup
- Compose a new email in the Mail app.
- Send it to any email address.
- Select the new localhost account as the `From` address.
- You should receive a follow-up email processed by your local server.
