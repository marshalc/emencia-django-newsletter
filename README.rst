Emancia Django Newsletter - Clean rewrite  (EDN)
================================================

A fresh approach to the codebase for the popular newsletter system, but written in terms I can understand. I realise
this breaks most people's approach to things, but I need to have a maintainable (by me, and my limitations) newsletter
system for a production site, and keeping up with the random directions and patching every once in a while is not
working for me.

Plan
----

Starting from a clean Django 1.7 (Python 2.7) base, import the original emencia elements, deconstruct them, and
gradually rebuild to a working (if more basic) state. From there, add to the feature list, which will be maintained
in the Github issues list.

Functionality
-------------

Contacts
 * Email and name
 * Ability to have contact click a link in an automated email to validate their email address (verified contact)
 * Mark contact as a test contact for sending draft messages to (tester)

 * Dropped:
  * Set valid contact - We'll un-verify the contact if the email address becomes invalid, and set the date of
    verification request so that we can automatically (maybe?) clean these dead addresses out later
  * Set as subscriber - If they're on a list, they're a subscriber
  * Export contact as a VCard. Maybe add later.
  * Import and Export. This needs to come back again soon, but can be skipped for the moment.


Mailing List
 * Name and description
 * Subscribers - Contacts on this list have subscribed and still want mailings
 * Unsubscribers - Contacts on this list were subscribed, but no longer want mailings

 * Dropped
  * Visible to the public? Assuming it's all public
  * MailingListSegments - unknown purpose

Newsletter
 * Name and HTML/Plain text content
 * Display content via URL on website
 * Allow links to be converted to tracked links (utils/newsletter.py). Handle this in the rendering of the newsletter
 * Embed a tracking image into the HTML version of the newsletter sent. Not optional.
 * Convert included links (in the html href) to tracked links. Optional via setting. Includes anchor tags.
 * Automatically include an unsubscribe link in each newsletter. Not optional!
 * Use a django template to format the message

 * Dropped
  * URL in content for inclusion
  * Unique identifier string in name
  * Public - assuming it's all public. If we need private (and therefore password protected) we'll add it later
  * Attachments. Add it back in later.
  * Workgroups. Not a clear purpose for use yet.
  * Internationalisation. I'll just admit this isn't something I know a lot about, nor have a use for presently.

Statistics
 * Want basic tracking of messages sent, and messages opened to be working.

