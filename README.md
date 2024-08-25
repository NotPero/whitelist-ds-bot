# whitelist-ds-bot

Introduction to the Whitelist Bot
The whitelist bot is designed to manage an automated whitelist process on a Discord server. Users can complete a quiz to obtain whitelist roles, or a designated moderator can manually grant the whitelist to a specific user.
1. Automated Whitelist Process: Users answer a quiz to gain access to the whitelist.
2. Manual Whitelist Assignment: Moderators can manually grant the whitelist to a user using a special command.
3. Logging: All relevant actions, such as whitelist attempts and manual assignments, are logged in a designated channel.


1. TOKEN
Description: The token for the Discord bot.
Usage: Enter the bot token you obtained when you created the bot on Discord.
Example: "TOKEN": ""
2. COMMAND
Description: The name of the command that users must use to start the whitelist process.
Usage: You can customize this name to anything you like, such as "whitelist" or "join".
Example: "COMMAND": "whitelist"
3. ROLE_ID
Description: The IDs of the roles that will be granted to users who successfully pass the whitelist.
Usage: Enter the IDs of the Discord roles you want to assign. You can find role IDs by enabling developer mode on Discord and right-clicking on the roles.
Example: "ROLE_ID": [123456789012345678, 987654321098765432]
4. NUM_QUESTIONS
Description: The number of questions that will be asked during the whitelist process.
Usage: Specify the number of questions users will need to answer to complete the whitelist process.
Example: "NUM_QUESTIONS": 3"
5. PASS_THRESHOLD
Description: The pass threshold, represented as a fraction (e.g., 0.8 means 80%).
Usage: Indicate the minimum percentage of correct answers required to pass the whitelist.
Example: "PASS_THRESHOLD": 0.8"
6. LANGUAGE
Description: The default language for the bot.
Usage: Specify the language code (e.g., "en" for English, "it" for Italian) that the bot will use for messages.
Example: "LANGUAGE": "en"
7. LOG_CHANNEL_ID
Description: The ID of the Discord channel where the bot will log whitelist-related activities.
Usage: Enter the ID of the channel where you want the bot to send logs. You can obtain the channel ID by enabling developer mode on Discord and right-clicking on the channel.
Example: "LOG_CHANNEL_ID": 123456789012345678"
8. givewhitelist
Description: A section that configures the command for manually granting the whitelist.
Fields:
COMMAND: The name of the command that manually grants the whitelist.
ALLOWED_ROLES: A list of role IDs that are authorized to use this command.
Usage:
COMMAND: Customize the name of the command, such as "givewhitelist" or "grantwhitelist".
ALLOWED_ROLES: Specify which roles are allowed to use this command.
