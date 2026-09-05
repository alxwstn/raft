# RAFT analysis

Automates the RAFT manual data flows. Note that this is a proof of concept that runs on a personal machine. This POC
shows that the manual spreadsheet workflow utilized by RAFT interns could be automated if there was desire to do so in the future.

Implements whiteboard tracking and team tracking spreadsheet analysis as documented here:
- [How to Update Whiteboard Totals](https://docs.google.com/document/d/1vbx5byVoYNURoynHmWhI8mvFU21mnZV_)
- [How to update Team Tracking Totals](https://docs.google.com/document/d/1J0R-ZWudCTxEuxFDn_6jt01F-qXJzaGC1krsJKIcAW8)

## Credentials
Create a new OAuth 2.0 Client (per machine) and save the key in a file named credentials.json at the project root.
[link to google cloud console for the raft-automation project](https://console.cloud.google.com/apis/credentials?chat=true&project=raft-automation)
Then add the user's email for testing [here](https://console.cloud.google.com/auth/audience?chat=true&project=raft-automation) under "Test users" 

## Resources

- [virtual env cheat sheet](https://gist.github.com/ryanbehdad/858b47b54be441a684efb7ae6ca98a75)
  - For git-bash on windows, use `. venv/Scripts/activate`. Explanation [here](https://deborahwrites.co.uk/blog/activate-virtualenv-git-bash-windows/).
- [pandas cheat sheet](https://pandas.pydata.org/Pandas_Cheat_Sheet.pdf)
