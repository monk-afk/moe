# Privacy Policy

Effective Date: November 13, 2026

## Introduction

SquareOne ("we", "our", "us") operates møe ("Moe", "the Chatbot", "the Application"). This Privacy Policy explains what information Moe processes, why it is processed, how long it is retained, and how users may request access to or deletion of information associated with them.

## Information We Process

Moe processes limited Discord API data needed to provide its chat functionality:

- **Message content:** Eligible messages sent in Discord guild channels accessible to Moe. Only the first 30 words of each eligible message are added to Moe's recent conversation context.
- **Discord identifiers:** Guild IDs and channel IDs are used to separate conversation context and store guild configuration. A Discord user ID may be used for reply-specific context or retained in Moe's ignore list.
- **Guild configuration:** The channel ID selected as a guild's designated reply channel.

Depending on applicable law and the contents of a message, Discord identifiers and message content may be considered personal information.

Moe does not process direct messages. Messages beginning with Moe's command prefix are not added to conversation context.

## How We Use Information

Moe uses this information only to:

- Maintain a short, recent conversation context and generate relevant replies.
- Keep guild configuration separate between Discord guilds.
- Maintain an ignore list for abuse and spam prevention.
- Operate and secure the Chatbot.

Moe does not use Discord message content to train or fine-tune machine-learning or artificial-intelligence models. Moe does not profile users or use their information for advertising, eligibility decisions, or discrimination.

Moe runs the DialoGPT model locally. Message content is not transmitted to Microsoft or Hugging Face for response generation.

## Storage Format and Security

Message content retained for conversation context is converted into integer tokenizer token IDs. These token IDs are not encryption and can be decoded using the corresponding tokenizer.

Moe's stored data file is encrypted at rest using Fernet encryption. The data is decrypted into process memory while Moe is running so that the Chatbot can operate. Moe does not routinely write message content to its application logs.

We take reasonable measures to protect information from unauthorized access, use, alteration, disclosure, or destruction. No method of electronic storage or transmission is completely secure.

## Retention

Each channel or reply-specific conversation context is limited to the most recent 12 tokenized message entries and no more than 100 model tokens. The older limit is discarded automatically when either limit is exceeded.

Messages added to a channel context are stored under the channel ID without an associated author ID. Messages in reply-specific context may be stored under the replying user's Discord ID.

When a member leaves a guild, reply-specific context associated with that user's ID is removed from that guild. Tokens already merged into a channel context cannot be selected by author because the author ID is not retained with them; they remain only until displaced by the normal context limits, cleared by a guild administrator, or deleted when Moe leaves the guild.

Guild configuration and channel context are deleted when Moe is removed from the guild.

A user ID placed on the ignore list is retained only to enforce that restriction and prevent abuse or spam. It remains until a guild administrator removes the restriction. The `forgetme` command does not remove an ignore-list entry.

## Access and Deletion

Users may use Moe's `forgetme` command to remove reply-specific conversation context associated with their Discord user ID across guilds. Because channel context does not retain author IDs, `forgetme` does not identify or remove individual contributions already merged into a channel context.

Authorized guild administrators may remove a user's reply-specific context or clear the guild's stored context and configuration using Moe's administrative commands.

To request access to, correction of, or deletion of information associated with your Discord user ID, contact us at admin@monk.moe. Please include your Discord user ID so that we can identify the applicable record.

## Disclosure of Information

We do not sell, license, or disclose Discord API data for advertising or data-broker purposes. Information may be processed by service providers only as necessary to host and operate Moe, or disclosed when required by applicable law.

## Children's Privacy

Moe is not intended for anyone under the age of 13 or under the minimum age required to use Discord in their jurisdiction, if higher. We do not knowingly target or provide Moe to users below that age.

## Changes to This Privacy Policy

We may update this Privacy Policy when Moe or its data practices change. Updated versions will be published with a new effective date.

## Contact Us

For questions or privacy requests, contact us at admin@monk.moe.
