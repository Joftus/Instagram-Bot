README:

IN COLLABORATION WITH: Alex Loftus
This project aims to provide useful analytics about an Instagram account.



FEATURES:
- Find users that have posted in both:
    + Hashtag & Hashtag
    + Hashtag & Location
- Scrape marketplace websites to generate stats and return
    + Top 10 most profitable account types
    + Optimal follower levels to sell at



REQUIREMENTS (PIP INSTALL):
- numpy
- selenium
    + ChromeDriver
- explicit
- requests
- https://github.com/jacexh/pyautoit/archive/master.zip



TO DO:
- TODO: Set up resolve actions correctly
- TODO: Move over combo mash from IGActionAutomator



PARAMETER STRUCTURE:
"username" "password" "actionString" "inspoAccountsSepBy|" "inspoHashtagsSepBy|"

username: User intstagram username
password: User instagram password
actionString: string of [y/n] characters that represent what actions should be performed
    + [0]: debugMethod
inspoAccountsSepBy|: List of accounts that the main account reposts photos from
inspoHashtagsSepBy|: List of hashtags that the main account reposts photos from

EXAMPLES:
"coppenmor" "Chicago2019!" "n" "smloveforyou|memedividual|kalesalad" "meme|memes|dankmemes"
