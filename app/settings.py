from themes import get_theme

# Overall settings. If you're running this locally and don't provide
PUBLIC = False
PUBLIC_USER = ""

# If you provide a key, chose what stats pull in data from private repos
ALLOW_PRIVATE_REPOS = False
ALLOW_PRIVATE_COMMITS = True
ALLOW_PRIVATE_REQUESTS = True
ALLOW_PRIVATE_REVIEWS = True
ALLOW_PRIVATE_ISSUES = True

# Graph Settings
SHOW_TOP_LANGUAGES = True
DISPLAY_STARS = True
DISPLAY_REPOS = True
DISPLAY_COMMITS = True
DISPLAY_REQUESTS = True
DISPLAY_REVIEWS = True
DISPLAY_ISSUES = True

# Image Settings
TITLE_FONT_SIZE = 32
TITLE_LINE_HADJ = 10
TITLE_LINE_VADJ = 8
TITLE_LINE_WIDTH = 3
TITLE_USE_REAL_NAME = True

ITEM_FONT_SIZE = 14
ITEM_IMG_SIZE = 32
ITEM_STARTING_Y = 70
ITEM_STARTING_X = 40
ITEM_VADJ = 45
ITEM_TEXT_HADJ = 4

IMAGE_BORDER_RADIUS = 20
IMAGE_THEME = get_theme("dark")
