## Critique: "Set up a custom sending domain"

### What's working

This is a well-built procedural article, and most of the hard choices are already right:

- **Benefit before mechanics.** The opening sentence says why a reader should care, in their language ("fewer of them land in spam"), before any UI appears. It also hedges honestly — "fewer," not "no more" — which is the correct claim to make about email deliverability.
- **Cost stated up front.** Time and the DNS delay are disclosed in the intro rather than sprung on the reader at step 4.
- **Prerequisites separated.** "Before you start" does real work: it lets a reader who lacks DNS access stop before wasting effort.
- **Four steps, imperative, with bold UI paths.** Right granularity. No step bundles two decisions.
- **The closing scope note.** "Invoices you've already sent are not affected" answers an anxious question the reader hasn't asked yet. That's the instinct of someone who has read support tickets.

The problems below are gaps in coverage, not failures of craft.

---

### Major

**1. Step 4 dead-ends. There is no failure path.**

"If verification fails, wait an hour and try again" tells the reader what to do once. It doesn't say what to do when the second attempt also fails — which, given the intro's own "up to 48 hours," is the likely outcome for many readers. The article's two time figures also contradict each other in tone: the intro prepares the reader for two days, step 4 implies an hour.

A reader who fails twice now has no instruction and a live suspicion that they typed something wrong. Needed: a ceiling and an escalation ("If verification still fails after 48 hours, the records were probably entered incorrectly — check X, or contact support"). This is the single biggest gap, because it's the moment the article abandons the reader.

**2. "Ask them to do steps 3 and 4" hands off a step they can't do.**

Step 4 happens inside Ledgerly ("Back in Ledgerly, select **Verify**"). The web person who manages the reader's DNS almost certainly has no Ledgerly login. As written, the instruction either breaks or quietly asks the reader to share account credentials with a contractor.

The clean split is: delegate step 3, then do step 4 yourself once they confirm the records are in. That also usefully implies the coordination the reader needs to plan for.

**3. The audience's two real stumbling blocks are both unaddressed.**

For non-technical small-business owners specifically:

- *"Sign in to your DNS provider"* assumes the reader knows who that is. Many don't — it's often whoever built the site years ago, or bundled with their registrar. "Before you start" flags that they need DNS access but gives no way to find out whether they have it or who holds it.
- *"add each record exactly as shown"* is the sentence where "exactly" misleads. Many DNS control panels auto-append the domain to the host/name field, so pasting the value as shown produces `billing.yourcompany.com.yourcompany.com`. This is the most common cause of failed verification in this entire genre of setup, and it's the specific thing a reader cannot diagnose alone.

Both are content additions rather than rewrites, and either one would do more for completion rates than any sentence-level change in the piece.

---

### Moderate

**4. Step 2 is ambiguous because the intro primed the wrong value.** The intro's example is an email address (`billing@yourcompany.com`); step 2 says "Enter your domain." A reader following along may paste the address. Say what to enter and what not to — "Enter your domain only (`yourcompany.com`), not a full email address."

**5. The From address is left dangling.** The intro raises `billing@yourcompany.com`, but after verification the reader is only told invoices send "from your domain." Which mailbox? Can they choose it? Where do replies go? The intro created a specific expectation the ending doesn't close.

**6. Terminology drifts across three words for one thing.** The intro says DNS providers "publish" changes; step 4 says changes "spread." Avoiding "propagate" is a good call for this audience, but pick one plain verb and reuse it. Repetition reads as consistency here, not as poverty.

---

### Minor

**7. "## Steps" is an empty heading.** It carries no information and adds no scannability a numbered list doesn't already have. Either drop it or name the task.

**8. The title is product vocabulary, not reader vocabulary.** A small-business owner searches "invoices going to spam" or "send invoices from my own email," not "custom sending domain." The intro's first sentence rescues this for in-page search, but consider whether the title or subtitle can carry the symptom as well as the feature name.

**9. "About 15 minutes" quietly assumes the reader does it all themselves.** Once step 3 is delegated, elapsed time is however long the web person takes. Worth a clause.

---

### Questions for you

- Is this feature plan-gated? If so, the gate belongs in "Before you start," which is currently the only place a reader can be stopped cheaply.
- Does Ledgerly's verify screen surface *which* record failed? If it does, say so in step 4 — it converts a guessing problem into a checking problem.
- Is "three CNAME records" stable? It's good concrete detail, but it will silently go stale if the setup ever adds a fourth.