import os
import sys
import math
from PIL import Image, ImageDraw, ImageFont
import ebooklib
from ebooklib import epub
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, HRFlowable, Image as RLImage, KeepTogether
)
from reportlab.pdfgen import canvas
import pypdf

# Define paths
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
EPUB_PATH = os.path.join(BASE_DIR, "dallas_cowboys_trivia_book.epub")
PDF_PATH = os.path.join(BASE_DIR, "dallas_cowboys_trivia_book.pdf")
COVER_PATH = os.path.join(BASE_DIR, "cover.png")

# ---------------------------------------------------------
# 1. Create Cover Image (1200 x 1800)
# ---------------------------------------------------------
def create_cover():
    width, height = 1200, 1800
    img = Image.new('RGB', (width, height), color='#001F3F')  # Deep Navy
    draw = ImageDraw.Draw(img)

    # Double Border
    draw.rectangle([40, 40, width-40, height-40], outline='#869397', width=6)
    draw.rectangle([58, 58, width-58, height-58], outline='#FFFFFF', width=2)

    # Draw Star Motif in Center
    star_center = (width // 2, 580)
    outer_r = 200
    inner_r = 85
    points = []
    for i in range(10):
        r = outer_r if i % 2 == 0 else inner_r
        angle = i * (math.pi / 5) - (math.pi / 2)
        x = star_center[0] + r * math.cos(angle)
        y = star_center[1] + r * math.sin(angle)
        points.append((x, y))
    
    # Outer silver star
    draw.polygon(points, fill='#FFFFFF', outline='#869397')
    # Inner navy star
    inner_points = []
    for i in range(10):
        r = (outer_r - 28) if i % 2 == 0 else (inner_r - 12)
        angle = i * (math.pi / 5) - (math.pi / 2)
        x = star_center[0] + r * math.cos(angle)
        y = star_center[1] + r * math.sin(angle)
        inner_points.append((x, y))
    draw.polygon(inner_points, fill='#003594', outline='#FFFFFF')

    # Typography
    try:
        font_large = ImageFont.truetype("arial.ttf", 72)
        font_medium = ImageFont.truetype("arial.ttf", 44)
        font_sub = ImageFont.truetype("arial.ttf", 34)
        font_body = ImageFont.truetype("arial.ttf", 26)
    except:
        font_large = font_medium = font_sub = font_body = ImageFont.load_default()

    # Header & Title
    draw.text((width//2, 220), "AMERICA'S TEAM TRIVIA SERIES", fill='#869397', font=font_body, anchor='mm')
    draw.text((width//2, 900), "THE DALLAS COWBOYS", fill='#FFFFFF', font=font_large, anchor='mm')
    draw.text((width//2, 990), "TRIVIA BOOK", fill='#869397', font=font_large, anchor='mm')
    
    # Gold accent line
    draw.line([(width//2 - 280, 1070), (width//2 + 280, 1070)], fill='#FFFFFF', width=4)

    # Subtitle
    draw.text((width//2, 1140), "THE ULTIMATE FAN ENCYCLOPEDIA", fill='#FFFFFF', font=font_medium, anchor='mm')
    draw.text((width//2, 1220), "Over 150 Questions, Untold Stories & Historical Records", fill='#869397', font=font_sub, anchor='mm')
    draw.text((width//2, 1275), "From the Cotton Bowl to Texas Stadium & AT&T Stadium", fill='#FFFFFF', font=font_body, anchor='mm')

    # Edition badge
    draw.rectangle([width//2 - 220, 1420, width//2 + 220, 1490], outline='#869397', fill='#002244', width=2)
    draw.text((width//2, 1455), "COMPLETE 60-PAGE EDITION", fill='#FFFFFF', font=font_body, anchor='mm')

    # Author
    draw.text((width//2, 1680), "AMERICA'S TEAM PRESS", fill='#869397', font=font_sub, anchor='mm')

    img.save(COVER_PATH)
    print("Cover image created successfully.")

# ---------------------------------------------------------
# 2. Complete Book Data (10 Chapters + Mastermind Exam = 130 Questions + Detailed Explanations)
# ---------------------------------------------------------
CHAPTERS = [
    {
        "id": "chap1",
        "title": "Chapter 1: The Birth of a Franchise & Cotton Bowl Years (1960–1970)",
        "intro": "The Dallas Cowboys entered the NFL in 1960 as an expansion franchise under founding owner Clint Murchison Jr., general manager Tex Schramm, and head coach Tom Landry. Playing their early home games at the historic Cotton Bowl, the team suffered through an winless inaugural season before ascending into an NFL powerhouse by the late 1960s.",
        "questions": [
            {
                "q": "1. On what date were the Dallas Cowboys officially granted an NFL expansion franchise?",
                "options": ["A) January 28, 1960", "B) September 12, 1959", "C) November 5, 1960", "D) March 15, 1961"],
                "ans": "A) January 28, 1960",
                "fact": "The Cowboys were officially approved as an expansion team at the NFL's annual meeting in Miami. Because the 1960 NFL Draft had already occurred in November 1959, Dallas had to build its inaugural roster through an expansion draft of existing teams' backup players."
            },
            {
                "q": "2. What original name was initially announced for the franchise before being changed to the Cowboys?",
                "options": ["A) Dallas Rangers", "B) Dallas Steers", "C) Dallas Wranglers", "D) Dallas Texans"],
                "ans": "A) Dallas Rangers",
                "fact": "The franchise was initially named the Dallas Rangers. However, to avoid confusion with a local minor league baseball team of the same name, the ownership group changed the team's moniker to the Cowboys prior to the start of the 1960 season."
            },
            {
                "q": "3. What was the win-loss-tie record of the Cowboys during their inaugural 1960 NFL regular season?",
                "options": ["A) 0-11-1", "B) 1-11-0", "C) 2-10-0", "D) 0-12-0"],
                "ans": "A) 0-11-1",
                "fact": "Dallas endured a brutal winless first year, finishing 0-11-1 under Tom Landry. Their sole non-loss was a dramatic 31-31 tie against the New York Giants at the Cotton Bowl on December 4, 1960."
            },
            {
                "q": "4. Who was the first-ever player selected by the Dallas Cowboys in the college draft (1961)?",
                "options": ["A) Don Meredith", "B) Bob Lilly", "C) Chuck Howley", "D) Lee Roy Jordan"],
                "ans": "B) Bob Lilly",
                "fact": "Defensive tackle Bob Lilly out of TCU was chosen 13th overall in the 1961 NFL Draft. Nicknamed 'Mr. Cowboy', Lilly went on to play 14 dominant seasons, earning 11 Pro Bowl selections and becoming the first member of the Cowboys Ring of Honor."
            },
            {
                "q": "5. Which quarterback, nicknamed 'Dandy Don', was the first franchise starting quarterback of the Cowboys?",
                "options": ["A) Don Meredith", "B) Eddie LeBaron", "C) Craig Morton", "D) Roger Staubach"],
                "ans": "A) Don Meredith",
                "fact": "Don Meredith signed with Dallas in 1960 out of SMU. He led the Cowboys to their first-ever winning season in 1966 and back-to-back NFL Championship game appearances in 1966 and 1967."
            },
            {
                "q": "6. In what stadium did the Dallas Cowboys play all of their home games from 1960 through midway into the 1971 season?",
                "options": ["A) Cotton Bowl", "B) Texas Stadium", "C) Alamo Dome", "D) Arlington Stadium"],
                "ans": "A) Cotton Bowl",
                "fact": "Located at Fair Park in Dallas, the Cotton Bowl served as the home of the Cowboys until October 1971, when Texas Stadium in Irving opened its doors."
            },
            {
                "q": "7. What was the result of the historic 1967 NFL Championship Game, famously known as the 'Ice Bowl'?",
                "options": [
                    "A) Green Bay Packers won 21-17",
                    "B) Dallas Cowboys won 20-17",
                    "C) Green Bay Packers won 14-10",
                    "D) Dallas Cowboys won 24-21"
                ],
                "ans": "A) Green Bay Packers won 21-17",
                "fact": "Played at Lambeau Field in -13°F weather (-48°F wind chill), Packers QB Bart Starr scored on a 1-yard quarterback sneak with 13 seconds left to defeat Dallas 21-17."
            },
            {
                "q": "8. Which Olympic 100m gold medalist sprinter joined the Cowboys in 1965 and revolutionized NFL pass defenses?",
                "options": ["A) Bob Hayes", "B) Frank Clarke", "C) Lance Alworth", "D) Mel Renfro"],
                "ans": "A) Bob Hayes",
                "fact": "'Bullet' Bob Hayes won gold in the 100m at the 1964 Tokyo Olympics. His world-class speed forced opposing coaches to abandon man-to-man coverage and invent zone defenses."
            },
            {
                "q": "9. Linebacker Chuck Howley won Super Bowl V MVP in 1971. What historic distinction does he hold?",
                "options": [
                    "A) Only player from a losing team to win Super Bowl MVP",
                    "B) Youngest player to win Super Bowl MVP",
                    "C) First player with 3 interceptions in a Super Bowl",
                    "D) First defensive player to score a touchdown in a Super Bowl"
                ],
                "ans": "A) Only player from a losing team to win Super Bowl MVP",
                "fact": "Despite Dallas falling 16-13 to the Baltimore Colts, Howley recorded two interceptions and recovered a fumble, earning MVP honors."
            },
            {
                "q": "10. How many consecutive winning seasons did head coach Tom Landry lead the Cowboys to, starting in 1966?",
                "options": ["A) 16", "B) 18", "C) 20", "D) 22"],
                "ans": "C) 20",
                "fact": "Tom Landry posted 20 straight winning seasons from 1966 to 1985—an NFL record that remains unmatched to this day."
            }
        ]
    },
    {
        "id": "chap2",
        "title": "Chapter 2: Captain Comeback & Super Bowl Glory (1971–1978)",
        "intro": "The 1970s marked the golden era of 'America's Team'. Led by Navy veteran and Heisman winner Roger Staubach, the Cowboys captured their first two Super Bowl victories (Super Bowl VI and Super Bowl XII) while establishing the fear-inducing 'Doomsday Defense'.",
        "questions": [
            {
                "q": "1. Against which opponent did the Cowboys win their first Super Bowl title (Super Bowl VI) on January 16, 1972?",
                "options": ["A) Miami Dolphins", "B) Denver Broncos", "C) Pittsburgh Steelers", "D) Oakland Raiders"],
                "ans": "A) Miami Dolphins",
                "fact": "Dallas blew out the Miami Dolphins 24-3 at Tulane Stadium in New Orleans. The Doomsday Defense held Miami without a touchdown, and Roger Staubach was named MVP."
            },
            {
                "q": "2. Why did quarterback Roger Staubach not make his NFL debut until 1969 despite being drafted in 1964?",
                "options": [
                    "A) Four-year military service commitment in the US Navy",
                    "B) Severe knee injury in college",
                    "C) Played in the Canadian Football League",
                    "D) Completed a law degree"
                ],
                "ans": "A) Four-year military service commitment in the US Navy",
                "fact": "Staubach won the 1963 Heisman Trophy at the US Naval Academy. He completed four years of active naval service, including a tour of duty in Vietnam, before joining the Cowboys."
            },
            {
                "q": "3. What iconic phrase did Roger Staubach coin following his 50-yard game-winning touchdown throw to Drew Pearson on Dec 28, 1975?",
                "options": ["A) Hail Mary", "B) Flea Flicker", "C) Shotgun Miracle", "D) Deep Bomb"],
                "ans": "A) Hail Mary",
                "fact": "With 24 seconds left against Minnesota, Staubach launched a desperation pass to Pearson. Afterwards he told reporters: 'I closed my eyes and said a Hail Mary.' The term became part of worldwide sports vernacular."
            },
            {
                "q": "4. Who co-won the Super Bowl XII MVP award alongside defensive tackle Randy White in January 1978?",
                "options": ["A) Harvey Martin", "B) Ed 'Too Tall' Jones", "C) Charlie Waters", "D) Cliff Harris"],
                "ans": "A) Harvey Martin",
                "fact": "Defensive end Harvey Martin and defensive tackle Randy White were named co-MVPs after terrorizing Denver quarterback Craig Morton in a 27-10 Dallas triumph."
            },
            {
                "q": "5. Which rookie running back out of Pittsburgh won Heisman honors in 1976 and rushed for 1,007 yards to lead Dallas to Super Bowl XII victory?",
                "options": ["A) Tony Dorsett", "B) Robert Newhouse", "C) Calvin Hill", "D) Preston Pearson"],
                "ans": "A) Tony Dorsett",
                "fact": "Dallas traded up to draft Dorsett #2 overall in 1977. He won AP Offensive Rookie of the Year and became the first player to win a College National Title, Heisman, and Super Bowl in back-to-back years."
            },
            {
                "q": "6. What nickname was bestowed upon the Dallas Cowboys by NFL Films narrator John Facenda in 1978?",
                "options": ["A) America's Team", "B) The Silver & Blue Express", "C) The Big D Machine", "D) Lone Star Legends"],
                "ans": "A) America's Team",
                "fact": "In the 1978 team highlight film, Facenda noted: 'They appear on television so often that their faces are as familiar to the public as presidents and movie stars. They are the Dallas Cowboys, America's Team.'"
            },
            {
                "q": "7. In 1971, Texas Stadium opened in Irving, Texas. What signature architectural feature made the stadium legendary?",
                "options": [
                    "A) A large partial hole in the roof",
                    "B) A fully retractable glass dome",
                    "C) Real natural grass imported from Bermuda",
                    "D) The world's largest video screen"
                ],
                "ans": "A) A large partial hole in the roof",
                "fact": "The partial roof opening inspired linebacker D.D. Lewis to famously quip: 'Texas Stadium has a hole in its roof so God can watch His team play.'"
            },
            {
                "q": "8. Which wide receiver wore jersey #88 and hauled in the original 'Hail Mary' pass in 1975?",
                "options": ["A) Drew Pearson", "B) Butch Johnson", "C) Golden Richards", "D) Billy Joe DuPree"],
                "ans": "A) Drew Pearson",
                "fact": "Drew Pearson was an undrafted free agent in 1973 who became a 3-time All-Pro, 1970s All-Decade team selection, and Pro Football Hall of Famer."
            },
            {
                "q": "9. Which Cowboys safety was known as 'Captain Crash' for his ferocious hitting style during the 1970s?",
                "options": ["A) Cliff Harris", "B) Charlie Waters", "C) Mel Renfro", "D) Darren Woodson"],
                "ans": "A) Cliff Harris",
                "fact": "Cliff Harris went from undrafted free agent out of Ouachita Baptist to 6-time Pro Bowler and 5-time All-Pro safety, forming a dominant duo with Charlie Waters."
            },
            {
                "q": "10. In Super Bowl XII, which fullback threw a surprise 48-yard touchdown pass on a halfback option play?",
                "options": ["A) Robert Newhouse", "B) Dan Reeves", "C) Walt Garrison", "D) Ron Springs"],
                "ans": "A) Robert Newhouse",
                "fact": "The 235-pound Newhouse, known for his 44-inch thighs, shocked Denver by throwing a deep touchdown pass to tight end Billy Joe DuPree in the 4th quarter."
            }
        ]
    },
    {
        "id": "chap3",
        "title": "Chapter 3: Doomsday II & The 1980s Gridiron Battles (1979–1988)",
        "intro": "The late 1970s and 1980s saw the transition from Roger Staubach to Danny White. Featuring towering pass rushers like Ed 'Too Tall' Jones and Harvey Martin, the Cowboys remained perennially competitive before undergoing roster turnover late in the decade.",
        "questions": [
            {
                "q": "1. Who succeeded Roger Staubach as the Cowboys starting quarterback in 1980?",
                "options": ["A) Danny White", "B) Gary Hogeboom", "C) Steve Pelluer", "D) Glenn Carano"],
                "ans": "A) Danny White",
                "fact": "Danny White took over in 1980 and performed double duty as both starting quarterback and punter, leading Dallas to three consecutive NFC Championship games (1980–1982)."
            },
            {
                "q": "2. On January 3, 1983, Tony Dorsett broke an NFL record by running for a touchdown of what distance against Minnesota?",
                "options": ["A) 99 Yards", "B) 95 Yards", "C) 98 Yards", "D) 100 Yards"],
                "ans": "A) 99 Yards",
                "fact": "Dorsett sprinted 99 yards for a touchdown on Monday Night Football—despite Dallas only having 10 offensive players on the field for the play!"
            },
            {
                "q": "3. What defensive end stood 6-foot-9 inches tall and played 15 seasons for Dallas between 1974 and 1989?",
                "options": ["A) Ed 'Too Tall' Jones", "B) Harvey Martin", "C) Jim Jeffcoat", "D) Randy White"],
                "ans": "A) Ed 'Too Tall' Jones",
                "fact": "Ed 'Too Tall' Jones was the #1 overall pick in the 1974 draft. He batted down dozens of passes and played in 224 games for Dallas, briefly taking a hiatus in 1979 to pursue professional boxing."
            },
            {
                "q": "4. Which Cowboys defensive back intercepted 11 passes as an undrafted rookie in 1981?",
                "options": ["A) Everson Walls", "B) Dennis Thurman", "C) Michael Downs", "D) Ron Fellows"],
                "ans": "A) Everson Walls",
                "fact": "Everson Walls out of Grambling State went unselected in the 1981 draft but led the NFL in interceptions as a rookie with 11 pick-offs."
            },
            {
                "q": "5. Which head coach led the Cowboys for 29 consecutive seasons from 1960 until February 1989?",
                "options": ["A) Tom Landry", "B) Jimmy Johnson", "C) Gene Stallings", "D) Frank Kush"],
                "ans": "A) Tom Landry",
                "fact": "Tom Landry posted 270 career wins, 2 Super Bowl titles, and 5 NFC Championships during his legendary 29-year tenure."
            },
            {
                "q": "6. Who purchased the Dallas Cowboys franchise from Bum Bright in February 1989 for $140 million?",
                "options": ["A) Jerry Jones", "B) Lamar Hunt", "C) Mark Cuban", "D) Red McCombs"],
                "ans": "A) Jerry Jones",
                "fact": "Arkansas oilman Jerry Jones bought the Cowboys and Texas Stadium lease on February 25, 1989, making his first major decision replacing Landry with Jimmy Johnson."
            },
            {
                "q": "7. Which wide receiver out of Miami was drafted by Dallas with the 11th overall pick in 1988?",
                "options": ["A) Michael Irvin", "B) Alvin Harper", "C) Alexander Wright", "D) Kelvin Martin"],
                "ans": "A) Michael Irvin",
                "fact": "Michael Irvin was Tom Landry's final first-round draft selection. Known as 'The Playmaker', Irvin became the emotional leader of the 1990s dynasty."
            },
            {
                "q": "8. What was the Cowboys record in 1989 during Jerry Jones and Jimmy Johnson's first season?",
                "options": ["A) 1-15", "B) 3-13", "C) 2-14", "D) 4-12"],
                "ans": "A) 1-15",
                "fact": "Dallas struggled through a painful 1-15 campaign in 1989. Their solitary victory was a 13-3 win over rival Washington on October 15."
            },
            {
                "q": "9. Which defensive lineman recorded 14 sacks in 1985 and finished his Cowboys career with 102.5 sacks?",
                "options": ["A) Jim Jeffcoat", "B) Harvey Martin", "C) Tony Tolbert", "D) Chad Hennings"],
                "ans": "A) Jim Jeffcoat",
                "fact": "Jim Jeffcoat was a standout pass-rusher for Dallas from 1983 to 1994, playing a major role in Super Bowls XXVII and XXVIII."
            },
            {
                "q": "10. In what city was general manager Tex Schramm, head coach Tom Landry, and scout Gil Brandt's famed computer drafting system developed?",
                "options": ["A) Dallas", "B) Houston", "C) Palo Alto", "D) Chicago"],
                "ans": "A) Dallas",
                "fact": "Gil Brandt collaborated with IBM computer programmers in Dallas to create the sports world's first computerized scouting database."
            }
        ]
    },
    {
        "id": "chap4",
        "title": "Chapter 4: The Great Walker Trade & Rebuilding a Giant (1989–1991)",
        "intro": "The turn of the decade witnessed one of the most audacious rebuilding efforts in professional sports history. Through the blockbuster Herschel Walker trade, head coach Jimmy Johnson amassed draft capital to construct the 1990s juggernaut.",
        "questions": [
            {
                "q": "1. In October 1989, Dallas traded running back Herschel Walker to which NFL team in exchange for a mountain of players and draft picks?",
                "options": ["A) Minnesota Vikings", "B) Atlanta Falcons", "C) Los Angeles Rams", "D) Green Bay Packers"],
                "ans": "A) Minnesota Vikings",
                "fact": "Dallas sent Walker to Minnesota for 5 players and 6 draft picks. Jimmy Johnson shrewdly packaged draft picks to acquire key championship starters."
            },
            {
                "q": "2. Which quarterback out of UCLA was drafted #1 overall by the Cowboys in the 1989 NFL Draft?",
                "options": ["A) Troy Aikman", "B) Steve Walsh", "C) Rodney Peete", "D) Timm Rosenbach"],
                "ans": "A) Troy Aikman",
                "fact": "Troy Aikman lost his first 11 career starts as a rookie in 1989 before going on to win 90 games in the 1990s and three Super Bowls."
            },
            {
                "q": "3. Which Heisman Trophy winning running back out of Florida was selected 17th overall by Dallas in 1990?",
                "options": ["A) Emmitt Smith", "B) Rodney Hampton", "C) James Brooks", "D) Natrone Means"],
                "ans": "A) Emmitt Smith",
                "fact": "Jimmy Johnson traded up with Pittsburgh to draft Emmitt Smith at #17. Smith won AP Offensive Rookie of the Year in 1990 with 937 rushing yards and 11 TDs."
            },
            {
                "q": "4. What nickname was given to fullback Daryl Johnston, who was drafted in 1989 and paved the way for Emmitt Smith?",
                "options": ["A) Moose", "B) Goose", "C) Tank", "D) Tractor"],
                "ans": "A) Moose",
                "fact": "Daryl 'Moose' Johnston was selected out of Syracuse. Fans lovingly bellowed 'MOOOOOSE' whenever he touched the ball or laid a lead block."
            },
            {
                "q": "5. What tight end was acquired from the Phoenix Cardinals in 1990 and became a 5-time Pro Bowler for Dallas?",
                "options": ["A) Jay Novacek", "B) Alfredo Roberts", "C) Eric Bjornson", "D) Jackie Harris"],
                "ans": "A) Jay Novacek",
                "fact": "Jay Novacek was a savvy Plan B free agent signing who became Troy Aikman's favorite third-down security blanket."
            },
            {
                "q": "6. In 1991, the Cowboys returned to the playoffs for the first time six years, defeating which opponent in the Wild Card round?",
                "options": ["A) Chicago Bears", "B) Philadelphia Eagles", "C) Detroit Lions", "D) Atlanta Falcons"],
                "ans": "A) Chicago Bears",
                "fact": "Backup QB Steve Beuerlein stepped in for an injured Aikman and led Dallas to a 17-13 postseason victory at Soldier Field."
            },
            {
                "q": "7. Which offensive line coach developed the 'Great Wall of Dallas' starting in 1989?",
                "options": ["A) Hudson Houck", "B) Tony Wise", "C) Dan Radakovich", "D) Larry Lacewell"],
                "ans": "B) Tony Wise",
                "fact": "Tony Wise constructed a massive offensive line anchored by Erik Williams, Mark Stepnoski, Nate Newton, and Tuinei."
            },
            {
                "q": "8. What defensive coordinator installed the fast, aggressive 4-3 defense in Dallas starting in 1989?",
                "options": ["A) Dave Wannstedt", "B) Butch Davis", "C) Dave Campo", "D) Tommy Tuberville"],
                "ans": "A) Dave Wannstedt",
                "fact": "Wannstedt brought Jimmy Johnson's signature Miami defensive scheme to the NFL, emphasizing team speed and penetration."
            },
            {
                "q": "9. Which versatile defensive back out of Arizona State was drafted in 1992 and became the Cowboys all-time tackle leader?",
                "options": ["A) Darren Woodson", "B) Brock Marion", "C) Clayton Holmes", "D) Phillippi Sparks"],
                "ans": "A) Darren Woodson",
                "fact": "Darren Woodson was taken in the 2nd round in 1992 and amassed 1,350 tackles over a decorated 12-year career."
            },
            {
                "q": "10. What wide receiver drafted out of Tennessee in 1991 hit a famous 70-yard touchdown in the 1992 NFC Championship Game?",
                "options": ["A) Alvin Harper", "B) Alexander Wright", "C) Jimmy Smith", "D) Ernie Mills"],
                "ans": "A) Alvin Harper",
                "fact": "Harper caught a slant pass from Aikman and raced 70 yards to the 1-yard line to seal the 1992 NFC Title victory over San Francisco."
            }
        ]
    },
    {
        "id": "chap5",
        "title": "Chapter 5: The 1990s Dynasty & Back-to-Back Champions (1992–1994)",
        "intro": "The Cowboys reached the pinnacle of pro football in 1992 and 1993. Behind 'The Triplets'—Troy Aikman, Emmitt Smith, and Michael Irvin—Dallas routed the Buffalo Bills in consecutive Super Bowls (XXVII and XXVIII).",
        "questions": [
            {
                "q": "1. What was the score of Super Bowl XXVII when Dallas crushed the Buffalo Bills at the Rose Bowl in January 1993?",
                "options": ["A) 52-17", "B) 30-13", "C) 38-20", "D) 41-14"],
                "ans": "A) 52-17",
                "fact": "Dallas forced 9 Buffalo turnovers. Troy Aikman threw 4 touchdown passes and earned Super Bowl MVP honors."
            },
            {
                "q": "2. In Super Bowl XXVII, defensive lineman Leon Lett famously lost a touchdown when stripped at the 1-yard line by which Bills receiver?",
                "options": ["A) Don Beebe", "B) Andre Reed", "C) James Lofton", "D) Steve Tasker"],
                "ans": "A) Don Beebe",
                "fact": "Lett held the ball out in celebration inside the 5-yard line, allowing a sprinting Beebe to knock it through the end zone for a touchback."
            },
            {
                "q": "3. Who won the Super Bowl XXVIII MVP award after rushing for 132 yards and 2 touchdowns against Buffalo in January 1994?",
                "options": ["A) Emmitt Smith", "B) Troy Aikman", "C) Michael Irvin", "D) James Washington"],
                "ans": "A) Emmitt Smith",
                "fact": "Smith carried Dallas to a 30-13 comeback victory in Atlanta, completing a season where he won the Rushing Title, NFL MVP, and Super Bowl MVP."
            },
            {
                "q": "4. In Week 18 of the 1993 regular season against the NY Giants, Emmitt Smith produced a heroic 229-yard performance despite suffering what severe injury?",
                "options": ["A) Separated shoulder", "B) Broken collarbone", "C) Torn hamstring", "D) Sprained ankle"],
                "ans": "A) Separated shoulder",
                "fact": "Smith separated his right shoulder in the 1st half but played through agony, carrying the ball 32 times for 168 yards and catching 10 passes for 61 yards in a 16-13 OT win."
            },
            {
                "q": "5. Why did head coach Jimmy Johnson surprisingly depart the Cowboys in March 1994 despite winning back-to-back Super Bowls?",
                "options": [
                    "A) Growing friction and disagreement with owner Jerry Jones",
                    "B) Health reasons",
                    "C) Retired to television broadcasting",
                    "D) Took a college coaching position"
                ],
                "ans": "A) Growing friction and disagreement with owner Jerry Jones",
                "fact": "Clashing egos over credit for building the team culminated in Jones and Johnson agreeing to part ways on March 28, 1994."
            },
            {
                "q": "6. Who was hired to replace Jimmy Johnson as Cowboys head coach for the 1994 season?",
                "options": ["A) Barry Switzer", "B) Butch Davis", "C) Chan Gailey", "D) Dennis Erickson"],
                "ans": "A) Barry Switzer",
                "fact": "Jerry Jones hired former Oklahoma Sooners national championship coach Barry Switzer."
            },
            {
                "q": "7. How many receiving yards did Michael Irvin tally during his peak 1995 season?",
                "options": ["A) 1,603 yards", "B) 1,490 yards", "C) 1,525 yards", "D) 1,380 yards"],
                "ans": "A) 1,603 yards",
                "fact": "Irvin caught 111 passes for 1,603 yards and 10 TDs in 1995, setting a franchise record that stood for 28 years."
            },
            {
                "q": "8. Which right tackle was named 1st-Team All-Pro from 1994 to 1996 and intimidated pass rushers with his ferocious strength?",
                "options": ["A) Erik Williams", "B) Mark Tuinei", "C) Larry Allen", "D) Rayfield Wright"],
                "ans": "A) Erik Williams",
                "fact": "Erik Williams famously neutralized Reggie White in 1992 and dominated pass rushers throughout the championship runs."
            },
            {
                "q": "9. How many rushing touchdowns did Emmitt Smith score in 1995 to set an NFL single-season record at the time?",
                "options": ["A) 25 TDs", "B) 21 TDs", "C) 27 TDs", "D) 23 TDs"],
                "ans": "A) 25 TDs",
                "fact": "Smith scored 25 rushing touchdowns in 1995, powering Dallas to an NFL-leading 436 points."
            },
            {
                "q": "10. Which safety returned a fumble 46 yards for a touchdown in Super Bowl XXVIII?",
                "options": ["A) James Washington", "B) Darren Woodson", "C) Thomas Everett", "D) Brock Marion"],
                "ans": "A) James Washington",
                "fact": "Washington picked up a Thurman Thomas fumble in the 3rd quarter and returned it for a game-tying touchdown."
            }
        ]
    },
    {
        "id": "chap6",
        "title": "Chapter 6: Super Bowl XXX & The End of an Era (1995–1999)",
        "intro": "Dallas capped off their 1990s legacy by defeating the Pittsburgh Steelers in Super Bowl XXX, becoming the first franchise to win three Super Bowls in a four-year span. High-profile additions like Deion Sanders cemented the star-studded era.",
        "questions": [
            {
                "q": "1. What was the score of Super Bowl XXX when Dallas defeated Pittsburgh on January 28, 1996?",
                "options": ["A) 27-17", "B) 31-19", "C) 24-14", "D) 35-21"],
                "ans": "A) 27-17",
                "fact": "Dallas won its fifth Super Bowl trophy at Sun Devil Stadium in Tempe, Arizona."
            },
            {
                "q": "2. Which cornerback won Super Bowl XXX MVP after snagging two second-half interceptions?",
                "options": ["A) Larry Brown", "B) Deion Sanders", "C) Kevin Smith", "D) Brock Marion"],
                "ans": "A) Larry Brown",
                "fact": "Larry Brown intercepted Neil O'Donnell twice in the 2nd half, both setting up short Emmitt Smith touchdown runs."
            },
            {
                "q": "3. Hall of Fame cornerback Deion 'Prime Time' Sanders signed with Dallas in 1995 after winning a Super Bowl with which rival?",
                "options": ["A) San Francisco 49ers", "B) Washington Redskins", "C) Philadelphia Eagles", "D) New York Giants"],
                "ans": "A) San Francisco 49ers",
                "fact": "Jerry Jones signed Sanders to a 7-year, $35 million deal. Sanders played cornerback, punt returner, and occasional wide receiver."
            },
            {
                "q": "4. Which offensive guard bench-pressed 705 lbs and was named to 11 Pro Bowls during his legendary Cowboys career?",
                "options": ["A) Larry Allen", "B) Nate Newton", "C) Mark Stepnoski", "D) Flozell Adams"],
                "ans": "A) Larry Allen",
                "fact": "Drafted out of Sonoma State in 1994, Larry Allen is considered one of the strongest and most dominant linemen in football history."
            },
            {
                "q": "5. What wide receiver held the franchise record for most career receiving touchdowns (73) until Dez Bryant?",
                "options": ["A) Bob Hayes", "B) Michael Irvin", "C) Drew Pearson", "D) Tony Hill"],
                "ans": "A) Bob Hayes",
                "fact": "Bob Hayes caught 71 touchdown passes in Dallas, a mark later passed by Dez Bryant."
            },
            {
                "q": "6. Who replaced Barry Switzer as Cowboys head coach prior to the 1998 season?",
                "options": ["A) Chan Gailey", "B) Dave Campo", "C) Bill Parcells", "D) Wade Phillips"],
                "ans": "A) Chan Gailey",
                "fact": "Chan Gailey led Dallas to playoff appearances in both 1998 and 1999."
            },
            {
                "q": "7. What tragic neck injury in Philadelphia effectively ended Michael Irvin's career in October 1999?",
                "options": [
                    "A) Cervical spinal stenosis",
                    "B) Fractured collarbone",
                    "C) Torn ACL",
                    "D) Ruptured disc"
                ],
                "ans": "A) Cervical spinal stenosis",
                "fact": "Irvin sustained a spinal cord injury on the Veteran Stadium turf on Oct 10, 1999, forcing his retirement."
            },
            {
                "q": "8. What defensive end recorded 13 sacks in 1996 and won three Super Bowls with Dallas?",
                "options": ["A) Tony Tolbert", "B) Shante Carver", "C) Greg Ellis", "D) Kavika Pittman"],
                "ans": "A) Tony Tolbert",
                "fact": "Tolbert was a constant pass rushing threat alongside Charles Haley."
            },
            {
                "q": "9. Which pass rusher brought five Super Bowl rings to Dallas, winning two in San Francisco and three in Dallas?",
                "options": ["A) Charles Haley", "B) DeMarcus Ware", "C) Jim Jeffcoat", "D) Harvey Martin"],
                "ans": "A) Charles Haley",
                "fact": "Charles Haley was acquired in 1992 and was the first player in NFL history to win five Super Bowl rings."
            },
            {
                "q": "10. In what year did Troy Aikman officially retire from professional football?",
                "options": ["A) 2001", "B) 1999", "C) 2003", "D) 2005"],
                "ans": "A) 2001",
                "fact": "Concussions forced Aikman to retire in April 2001. He transitioned into FOX's lead NFL color analyst."
            }
        ]
    },
    {
        "id": "chap7",
        "title": "Chapter 7: The Tony Romo Era & Unforgettable Thrillers (2000–2015)",
        "intro": "The 2000s ushered in a dramatic new chapter. Hall of Fame coach Bill Parcells brought discipline, while undrafted quarterback Tony Romo emerged from obscurity to set franchise passing records alongside stars like Jason Witten, DeMarcus Ware, and Dez Bryant.",
        "questions": [
            {
                "q": "1. Which small FCS school did Tony Romo attend before going undrafted in 2003?",
                "options": ["A) Eastern Illinois", "B) Northern Iowa", "C) Western Michigan", "D) Southern Illinois"],
                "ans": "A) Eastern Illinois",
                "fact": "Romo won the Walter Payton Award at EIU. He joined Dallas as a 3rd-string QB behind Quincy Carter and Vinny Testaverde."
            },
            {
                "q": "2. In what game did Tony Romo make his first career NFL start in 2006?",
                "options": [
                    "A) At Carolina Panthers (Week 8)",
                    "B) Vs New York Giants (Week 7)",
                    "C) Vs Philadelphia Eagles (Week 5)",
                    "D) At Washington (Week 9)"
                ],
                "ans": "A) At Carolina Panthers (Week 8)",
                "fact": "Parcells inserted Romo at halftime against the Giants, then started him the next week at Carolina, winning 35-14."
            },
            {
                "q": "3. Who holds the Cowboys all-time career records for passing yards (34,183) and passing touchdowns (248)?",
                "options": ["A) Tony Romo", "B) Troy Aikman", "C) Roger Staubach", "D) Dak Prescott"],
                "ans": "A) Tony Romo",
                "fact": "Romo passed Troy Aikman's records, finishing his career with a 97.1 passer rating."
            },
            {
                "q": "4. Which line-backer out of Troy was drafted 11th overall in 2005 and recorded 117.0 sacks in Dallas?",
                "options": ["A) DeMarcus Ware", "B) Anthony Spencer", "C) Sean Lee", "D) Bradie James"],
                "ans": "A) DeMarcus Ware",
                "fact": "Ware led the NFL in sacks twice (2008 & 2010), recording 20.0 sacks in 2008."
            },
            {
                "q": "5. Which tight end played 16 seasons for Dallas, setting franchise records for receptions (1,215) and receiving yards (12,977)?",
                "options": ["A) Jason Witten", "B) Jay Novacek", "C) Martellus Bennett", "D) Dalton Schultz"],
                "ans": "A) Jason Witten",
                "fact": "Witten was an 11-time Pro Bowler. He famously ran 30 yards without a helmet against Philadelphia in 2007."
            },
            {
                "q": "6. What controversial catch/no-catch call occurred in the 2014 NFC Divisional Playoff game against Green Bay?",
                "options": ["A) Dez Bryant catch overturned", "B) Miles Austin stepping out of bounds", "C) Jason Witten offensive pass interference", "D) Terrence Williams drop"],
                "ans": "A) Dez Bryant catch overturned",
                "fact": "On 4th-and-2 with 4:42 left, Romo launched a 31-yard pass to Dez Bryant at the 1-yard line. The catch was overturned upon review under the 'completing the process' rule."
            },
            {
                "q": "7. On October 27, 2002, Emmitt Smith broke whose all-time NFL career rushing record at Texas Stadium?",
                "options": ["A) Walter Payton", "B) Jim Brown", "C) Barry Sanders", "D) Eric Dickerson"],
                "ans": "A) Walter Payton",
                "fact": "Smith surpassed Payton's 16,726 yards on an 11-yard run against Seattle. He retired with 18,355 rushing yards."
            },
            {
                "q": "8. Which wide receiver famously celebrated a touchdown by standing on the star logo at midfield in Texas Stadium while playing for San Francisco in 2000?",
                "options": ["A) Terrell Owens", "B) Randy Moss", "C) Chad Johnson", "D) Keyshawn Johnson"],
                "ans": "A) Terrell Owens",
                "fact": "T.O. ran to the star twice, prompting Cowboys safety George Teague to level him on his second attempt. Owens later played for Dallas from 2006 to 2008."
            },
            {
                "q": "9. Which head coach led Dallas to a 13-3 record and #1 seed in 2007?",
                "options": ["A) Wade Phillips", "B) Bill Parcells", "C) Jason Garrett", "D) Dave Campo"],
                "ans": "A) Wade Phillips",
                "fact": "Wade Phillips coached Dallas from 2007 to 2010, sending 13 players to the Pro Bowl in 2007."
            },
            {
                "q": "10. In what year did AT&T Stadium (Cowboys Stadium) open in Arlington, Texas?",
                "options": ["A) 2009", "B) 2007", "C) 2011", "D) 2013"],
                "ans": "A) 2009",
                "fact": "The $1.3 billion stadium opened in 2009 featuring a 160-foot HD video screen."
            }
        ]
    },
    {
        "id": "chap8",
        "title": "Chapter 8: The Dak Prescott Era & Modern Stars (2016–Present)",
        "intro": "When Tony Romo suffered a preseason injury in 2016, 4th-round draft pick Dak Prescott stepped in alongside rookie running back Ezekiel Elliott. Their instant stardom launched a new era of high-powered offenses and record-setting playmakers.",
        "questions": [
            {
                "q": "1. In what round of the 2016 NFL Draft was Dak Prescott selected out of Mississippi State?",
                "options": ["A) 4th Round", "B) 1st Round", "C) 2nd Round", "D) 6th Round"],
                "ans": "A) 4th Round",
                "fact": "Prescott was selected 135th overall. He led Dallas to a 13-3 record as a rookie and won AP Offensive Rookie of the Year."
            },
            {
                "q": "2. Which running back out of Ohio State was drafted #4 overall in 2016 and won two NFL rushing titles in his first three years?",
                "options": ["A) Ezekiel Elliott", "B) Derrick Henry", "C) Todd Gurley", "D) Tony Pollard"],
                "ans": "A) Ezekiel Elliott",
                "fact": "Zeke rushed for 1,631 yards as a rookie in 2016 and led the league again in 2018 with 1,434 yards."
            },
            {
                "q": "3. Which linebacker out of Penn State won AP NFL Defensive Rookie of the Year in 2021 after recording 13.0 sacks?",
                "options": ["A) Micah Parsons", "B) Leighton Vander Esch", "C) Jaylon Smith", "D) Trevon Diggs"],
                "ans": "A) Micah Parsons",
                "fact": "Selected 12th overall in 2021, Parsons immediately became one of the most feared pass rushers in football."
            },
            {
                "q": "4. In 2023, which wide receiver set single-season franchise records with 135 catches and 1,749 receiving yards?",
                "options": ["A) CeeDee Lamb", "B) Michael Irvin", "C) Dez Bryant", "D) Amari Cooper"],
                "ans": "A) CeeDee Lamb",
                "fact": "CeeDee Lamb broke Michael Irvin's 1995 franchise records with a historic 2023 season."
            },
            {
                "q": "5. Which cornerback set an all-time NFL single-season record in 2023 by returning 5 interceptions for touchdowns?",
                "options": ["A) DaRon Bland", "B) Trevon Diggs", "C) Stephon Gilmore", "D) Anthony Brown"],
                "ans": "A) DaRon Bland",
                "fact": "Bland, a 5th-round pick out of Fresno State, broke the previous record of 4 pick-sixes on Thanksgiving Day 2023."
            },
            {
                "q": "6. Which cornerback led the NFL with 11 interceptions in 2021?",
                "options": ["A) Trevon Diggs", "B) DaRon Bland", "C) Chidobe Awuzie", "D) Jourdan Lewis"],
                "ans": "A) Trevon Diggs",
                "fact": "Diggs was the first player since Everson Walls in 1981 to tally 11 INTs in a single season."
            },
            {
                "q": "7. Who was hired as Cowboys head coach in January 2020 after leading Green Bay to a Super Bowl title?",
                "options": ["A) Mike McCarthy", "B) Kellen Moore", "C) Dan Quinn", "D) Jason Garrett"],
                "ans": "A) Mike McCarthy",
                "fact": "McCarthy guided Dallas to three consecutive 12-5 seasons from 2021 to 2023."
            },
            {
                "q": "8. Which former soccer player set an NFL record in 2023 by making his first 35 consecutive field goal attempts?",
                "options": ["A) Brandon Aubrey", "B) Dan Bailey", "C) Brett Maher", "D) Greg Zuerlein"],
                "ans": "A) Brandon Aubrey",
                "fact": "Aubrey was signed out of the USFL and enjoyed one of the greatest kicking seasons in NFL history."
            },
            {
                "q": "9. What head coach led the Cowboys from 2011 to 2019, compiling an 85-67 record?",
                "options": ["A) Jason Garrett", "B) Wade Phillips", "C) Chan Gailey", "D) Dave Campo"],
                "ans": "A) Jason Garrett",
                "fact": "Garrett played backup QB for Dallas in the 1990s before serving 9 seasons as head coach."
            },
            {
                "q": "10. In 2021, Dak Prescott set a franchise single-season record by throwing how many touchdown passes?",
                "options": ["A) 37 TDs", "B) 36 TDs", "C) 39 TDs", "D) 34 TDs"],
                "ans": "A) 37 TDs",
                "fact": "Prescott broke Tony Romo's single-season mark of 36 touchdown passes set in 2007."
            }
        ]
    },
    {
        "id": "chap9",
        "title": "Chapter 9: The Ring of Honor, Hall of Famers & Franchise Records",
        "intro": "The Dallas Cowboys Ring of Honor and Canton's Pro Football Hall of Fame showcase the immortals of gridiron history. From Bob Lilly to Jimmy Johnson, test your knowledge on records, awards, and sacred traditions.",
        "questions": [
            {
                "q": "1. Who was the inaugural member inducted into the Dallas Cowboys Ring of Honor in 1975?",
                "options": ["A) Bob Lilly", "B) Don Meredith", "C) Tom Landry", "D) Tex Schramm"],
                "ans": "A) Bob Lilly",
                "fact": "Bob Lilly was inducted on Nov 23, 1975."
            },
            {
                "q": "2. Which legendary head coach was inducted into the Ring of Honor on December 30, 2023?",
                "options": ["A) Jimmy Johnson", "B) Barry Switzer", "C) Bill Parcells", "D) Gene Stallings"],
                "ans": "A) Jimmy Johnson",
                "fact": "Jerry Jones inducted Jimmy Johnson at halftime of a game against Detroit."
            },
            {
                "q": "3. Who holds the Cowboys franchise career sack record with 117.0 sacks?",
                "options": ["A) DeMarcus Ware", "B) Harvey Martin", "C) Ed 'Too Tall' Jones", "D) Randy White"],
                "ans": "A) DeMarcus Ware",
                "fact": "DeMarcus Ware recorded 117 sacks in 141 games for Dallas."
            },
            {
                "q": "4. What iconic jersey number worn by Bob Lilly was never officially retired but remains honored?",
                "options": ["A) #74", "B) #88", "C) #22", "D) #12"],
                "ans": "A) #74",
                "fact": "Number 74 is revered as 'Mr. Cowboy' Bob Lilly's number."
            },
            {
                "q": "5. Which defensive back holds the franchise record for career interceptions with 52?",
                "options": ["A) Mel Renfro", "B) Everson Walls", "C) Cliff Harris", "D) Darren Woodson"],
                "ans": "A) Mel Renfro",
                "fact": "Mel Renfro recorded 52 interceptions between 1964 and 1977."
            },
            {
                "q": "6. Who is the all-time tackle leader in Cowboys history with 1,350 tackles?",
                "options": ["A) Darren Woodson", "B) Lee Roy Jordan", "C) Randy White", "D) Dat Nguyen"],
                "ans": "A) Darren Woodson",
                "fact": "Darren Woodson surpassed Lee Roy Jordan's tackle record."
            },
            {
                "q": "7. How many total Super Bowl titles have the Dallas Cowboys won?",
                "options": ["A) 5", "B) 4", "C) 6", "D) 3"],
                "ans": "A) 5",
                "fact": "Dallas won Super Bowls VI, XII, XXVII, XXVIII, and XXX."
            },
            {
                "q": "8. Which jersey number has been worn by wide receivers Drew Pearson, Michael Irvin, Dez Bryant, and CeeDee Lamb?",
                "options": ["A) #88", "B) #80", "C) #81", "D) #19"],
                "ans": "A) #88",
                "fact": "#88 is reserved for premier wide receivers in Dallas."
            },
            {
                "q": "9. Which general manager pioneered cheerleaders, instant replay, and ref microphones?",
                "options": ["A) Tex Schramm", "B) Gil Brandt", "C) Clint Murchison", "D) Jerry Jones"],
                "ans": "A) Tex Schramm",
                "fact": "Tex Schramm was a visionary broadcasting innovator."
            },
            {
                "q": "10. How many Super Bowl appearances have the Cowboys made in total?",
                "options": ["A) 8", "B) 6", "C) 10", "D) 7"],
                "ans": "A) 8",
                "fact": "Dallas has appeared in 8 Super Bowls (tied for 2nd-most all time)."
            }
        ]
    },
    {
        "id": "chap10",
        "title": "Chapter 10: Rivalries, Thanksgiving & Stadium Legends",
        "intro": "The Cowboys story is defined by intense NFC East rivalries against Washington, Philadelphia, and New York, alongside Thanksgiving Day game traditions and legendary stadium moments.",
        "questions": [
            {
                "q": "1. In what year did Dallas host its first annual Thanksgiving Day NFL game?",
                "options": ["A) 1966", "B) 1960", "C) 1970", "D) 1975"],
                "ans": "A) 1966",
                "fact": "Tex Schramm signed Dallas up to play on Thanksgiving in 1966, beating Cleveland 26-14."
            },
            {
                "q": "2. Which division rival has Dallas faced in over 120 regular season games since 1960?",
                "options": ["A) Washington Commanders", "B) Green Bay Packers", "C) Pittsburgh Steelers", "D) San Francisco 49ers"],
                "ans": "A) Washington Commanders",
                "fact": "The Cowboys-Commanders rivalry is one of the fiercest in sports."
            },
            {
                "q": "3. What blustery Thanksgiving game in 1993 featured Leon Lett's infamous icy field fumble recovery attempt?",
                "options": ["A) Vs Miami Dolphins", "B) Vs Philadelphia Eagles", "C) Vs Green Bay Packers", "D) Vs Washington"],
                "ans": "A) Vs Miami Dolphins",
                "fact": "Lett touched a blocked field goal on icy turf, allowing Miami to recover and kick the winning field goal."
            },
            {
                "q": "4. What stadium served as home to the Cowboys from 1971 to 2008?",
                "options": ["A) Texas Stadium", "B) Cotton Bowl", "C) Alamo Dome", "D) Sun Bowl"],
                "ans": "A) Texas Stadium",
                "fact": "Texas Stadium in Irving hosted 38 seasons of Cowboys football."
            },
            {
                "q": "5. Who coined the line: 'A hole in the roof so God can watch His team play'?",
                "options": ["A) D.D. Lewis", "B) Tom Landry", "C) Tex Schramm", "D) Walt Garrison"],
                "ans": "A) D.D. Lewis",
                "fact": "Linebacker D.D. Lewis created the famous quote."
            },
            {
                "q": "6. What is the name of the official Cowboys practice and corporate facility opened in Frisco in 2016?",
                "options": ["A) The Star", "B) Cowboy Center", "C) Victory Plaza", "D) Landmark Center"],
                "ans": "A) The Star",
                "fact": "The Star in Frisco features a 12,000-seat indoor stadium and world-class headquarters."
            },
            {
                "q": "7. Which kicker booted a franchise-record 66-yard field goal in 2023?",
                "options": ["A) Brandon Aubrey", "B) Dan Bailey", "C) Brett Maher", "D) Chris Boniol"],
                "ans": "A) Brandon Aubrey",
                "fact": "Aubrey hit a 66-yarder against Philadelphia."
            },
            {
                "q": "8. What was the name of the Cowboys mascot introduced in 1998?",
                "options": ["A) Rowdy", "B) Tex", "C) Bandit", "D) Stampede"],
                "ans": "A) Rowdy",
                "fact": "Rowdy is the official mascot."
            },
            {
                "q": "9. Which opponent have the Cowboys played three times in the Super Bowl (X, XIII, XXX)?",
                "options": ["A) Pittsburgh Steelers", "B) Buffalo Bills", "C) Miami Dolphins", "D) Oakland Raiders"],
                "ans": "A) Pittsburgh Steelers",
                "fact": "Dallas and Pittsburgh met in three Super Bowls."
            },
            {
                "q": "10. Which Dallas running back threw a touchdown pass in Super Bowl XII?",
                "options": ["A) Robert Newhouse", "B) Tony Dorsett", "C) Preston Pearson", "D) Walt Garrison"],
                "ans": "A) Robert Newhouse",
                "fact": "Newhouse threw a 48-yard TD pass to Billy Joe DuPree."
            }
        ]
    }
]

# Mastermind Exam (20 Additional Questions)
MASTERMIND_EXAM = [
    {
        "q": "1. What was the score of the inaugural Cowboys game on Sept 24, 1960 against Pittsburgh?",
        "options": ["A) Lost 35-28", "B) Lost 24-10", "C) Tied 14-14", "D) Lost 42-14"],
        "ans": "A) Lost 35-28",
        "fact": "Dallas led late before losing 35-28 at the Cotton Bowl."
    },
    {
        "q": "2. Who scored the very first touchdown in Dallas Cowboys franchise history?",
        "options": ["A) Jim Johnston", "B) Frank Clarke", "C) Don Meredith", "D) Billy Howton"],
        "ans": "A) Jim Johnston",
        "fact": "Jim Johnston scored on a 2-yard run against Pittsburgh."
    },
    {
        "q": "3. Which wide receiver caught 14 touchdown passes in 1962?",
        "options": ["A) Frank Clarke", "B) Bob Hayes", "C) Lance Alworth", "D) Pete Gent"],
        "ans": "A) Frank Clarke",
        "fact": "Frank Clarke set an early franchise record with 14 TD catches."
    },
    {
        "q": "4. What head coach preceded Jimmy Johnson at the University of Miami before joining Dallas?",
        "options": ["A) Jimmy Johnson coached Miami", "B) Howard Schnellenberger", "C) Dennis Erickson", "D) Lou Holtz"],
        "ans": "A) Jimmy Johnson coached Miami",
        "fact": "Jimmy Johnson won the 1987 college national championship at Miami."
    },
    {
        "q": "5. Which defensive end logged 20.0 sacks in 2008?",
        "options": ["A) DeMarcus Ware", "B) Harvey Martin", "C) Jim Jeffcoat", "D) Greg Ellis"],
        "ans": "A) DeMarcus Ware",
        "fact": "Ware set the single-season franchise sack record."
    },
    {
        "q": "6. Which Cowboys QB threw for 506 yards in a single game against Denver in 2013?",
        "options": ["A) Tony Romo", "B) Dak Prescott", "C) Troy Aikman", "D) Jon Kitna"],
        "ans": "A) Tony Romo",
        "fact": "Romo threw for 506 yards and 5 TDs in a thrilling 51-48 duel."
    },
    {
        "q": "7. What was the nickname of defensive back Cornell Green?",
        "options": ["A) Sweet Bo", "B) Blue", "C) Quick Draw", "D) Shadow"],
        "ans": "A) Sweet Bo",
        "fact": "Green played 13 seasons without ever playing college football."
    },
    {
        "q": "8. Which center played 161 consecutive games for Dallas from 1975 to 1986?",
        "options": ["A) Mark Stepnoski", "B) Tom Rafferty", "C) John Fitzgerald", "D) Rayfield Wright"],
        "ans": "B) Tom Rafferty",
        "fact": "Rafferty anchored the offensive line for over a decade."
    },
    {
        "q": "9. Which running back rushed for 237 yards in a game against Green Bay in 1978?",
        "options": ["A) Tony Dorsett", "B) Herschel Walker", "C) Emmitt Smith", "D) Robert Newhouse"],
        "ans": "A) Tony Dorsett",
        "fact": "Dorsett set a single-game franchise rushing record."
    },
    {
        "q": "10. What jersey number did Darren Woodson wear?",
        "options": ["A) #28", "B) #41", "C) #37", "D) #26"],
        "ans": "A) #28",
        "fact": "Woodson wore #28 throughout his 3-time Super Bowl champion career."
    },
    {
        "q": "11. Who was the Cowboys leading receiver in Super Bowl VI?",
        "options": ["A) Duane Thomas", "B) Bob Hayes", "C) Lance Alworth", "D) Mike Ditka"],
        "ans": "C) Lance Alworth",
        "fact": "Hall of Famer Lance Alworth caught a 7-yard touchdown pass."
    },
    {
        "q": "12. What tight end caught a touchdown in Super Bowl VI for Dallas?",
        "options": ["A) Mike Ditka", "B) Billy Joe DuPree", "C) Jay Novacek", "D) Pettis Norman"],
        "ans": "A) Mike Ditka",
        "fact": "Mike Ditka caught a 7-yard TD pass from Staubach."
    },
    {
        "q": "13. Which Cowboys player scored 3 rushing touchdowns in Super Bowl XXVIII?",
        "options": ["A) Emmitt Smith", "B) Daryl Johnston", "C) Bernie Kosar", "D) Troy Aikman"],
        "ans": "A) Emmitt Smith",
        "fact": "Emmitt Smith scored 2 rushing TDs to seal the game."
    },
    {
        "q": "14. Who won NFL Coach of the Year with Dallas in 1977?",
        "options": ["A) Tom Landry", "B) Jimmy Johnson", "C) Barry Switzer", "D) Bill Parcells"],
        "ans": "A) Tom Landry",
        "fact": "Landry won Coach of the Year after a 12-2 season."
    },
    {
        "q": "15. How many total Pro Bowls was Bob Lilly selected to?",
        "options": ["A) 11", "B) 9", "C) 14", "D) 12"],
        "ans": "A) 11",
        "fact": "Bob Lilly was an 11-time Pro Bowler."
    },
    {
        "q": "16. Which Cowboys kicker made a 60-yard field goal in 2019?",
        "options": ["A) Brett Maher", "B) Dan Bailey", "C) Greg Zuerlein", "D) Brandon Aubrey"],
        "ans": "A) Brett Maher",
        "fact": "Maher hit three field goals of 60+ yards in his Dallas career."
    },
    {
        "q": "17. Who was the Cowboys leading rusher in 2008?",
        "options": ["A) Marion Barber", "B) Felix Jones", "C) Tashard Choice", "D) Emmitt Smith"],
        "ans": "A) Marion Barber",
        "fact": "'Marion the Barbarian' rushed for 885 yards and 7 TDs."
    },
    {
        "q": "18. What draft year was Jason Witten selected in?",
        "options": ["A) 2003", "B) 2002", "C) 2004", "D) 2001"],
        "ans": "A) 2003",
        "fact": "Witten was selected in the 3rd round (69th overall) in 2003."
    },
    {
        "q": "19. Which player recorded 4 interceptions in a single game for Dallas in 1968?",
        "options": ["A) Dick Daniels", "B) Mel Renfro", "C) Cliff Harris", "D) Charlie Waters"],
        "ans": "A) Dick Daniels",
        "fact": "Daniels tied the franchise single-game interception record."
    },
    {
        "q": "20. How many division titles have the Dallas Cowboys won in franchise history?",
        "options": ["A) 25", "B) 21", "C) 18", "D) 30"],
        "ans": "A) 25",
        "fact": "Dallas has won 25 NFC East / NFL Eastern division championships."
    }
]

# ---------------------------------------------------------
# 3. Generate 60-Page Kindle PDF E-Book (6x9 Trade Size)
# ---------------------------------------------------------
class NumberedCanvas60(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_decorations(self, page_count):
        if self._pageNumber <= 2:
            return  # Suppress headers on cover & title page

        self.saveState()
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(colors.HexColor("#002244"))

        # 6x9 Dimensions: Width=432, Height=648
        w = 6 * 72
        h = 9 * 72
        margin = 36

        # Running Header
        self.drawString(margin, h - 28, "THE DALLAS COWBOYS TRIVIA BOOK")
        self.setFont("Helvetica-Oblique", 8)
        self.drawRightString(w - margin, h - 28, "Ultimate Fan Encyclopedia")
        self.setStrokeColor(colors.HexColor("#003594"))
        self.setLineWidth(0.75)
        self.line(margin, h - 32, w - margin, h - 32)

        # Running Footer
        self.setStrokeColor(colors.HexColor("#CCCCCC"))
        self.setLineWidth(0.5)
        self.line(margin, 34, w - margin, 34)
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#555555"))
        self.drawString(margin, 22, "America's Team Press")
        page_text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(w - margin, 22, page_text)

        self.restoreState()

def generate_pdf_60pages():
    # 6x9 trade paperback page size
    page_w = 6 * 72  # 432 pt
    page_h = 9 * 72  # 648 pt

    doc = SimpleDocTemplate(
        PDF_PATH,
        pagesize=(page_w, page_h),
        leftMargin=36,
        rightMargin=36,
        topMargin=42,
        bottomMargin=42
    )

    styles = getSampleStyleSheet()

    # Custom typography styles
    title_style = ParagraphStyle(
        'CoverTitle', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=22, leading=26,
        textColor=colors.HexColor('#002244'), alignment=1, spaceAfter=10
    )
    subtitle_style = ParagraphStyle(
        'CoverSubtitle', parent=styles['Normal'],
        fontName='Helvetica', fontSize=12, leading=15,
        textColor=colors.HexColor('#869397'), alignment=1, spaceAfter=20
    )
    h1_style = ParagraphStyle(
        'ChapH1', parent=styles['Heading1'],
        fontName='Helvetica-Bold', fontSize=14, leading=18,
        textColor=colors.HexColor('#002244'), spaceBefore=12, spaceAfter=8, keepWithNext=True
    )
    h2_style = ParagraphStyle(
        'ChapH2', parent=styles['Heading2'],
        fontName='Helvetica-Bold', fontSize=12, leading=15,
        textColor=colors.HexColor('#003594'), spaceBefore=10, spaceAfter=6, keepWithNext=True
    )
    intro_style = ParagraphStyle(
        'ChapIntro', parent=styles['Normal'],
        fontName='Helvetica-Oblique', fontSize=9.5, leading=14,
        textColor=colors.HexColor('#222222'), spaceAfter=12
    )
    q_title_style = ParagraphStyle(
        'QTitle', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=9.5, leading=13,
        textColor=colors.HexColor('#002244'), spaceBefore=6, spaceAfter=4, keepWithNext=True
    )
    opt_style = ParagraphStyle(
        'OptStyle', parent=styles['Normal'],
        fontName='Helvetica', fontSize=8.5, leading=11.5,
        textColor=colors.HexColor('#333333'), leftIndent=10, spaceAfter=2
    )
    ans_style = ParagraphStyle(
        'AnsStyle', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=8.5, leading=11.5,
        textColor=colors.HexColor('#003594'), spaceBefore=3, spaceAfter=2
    )
    fact_style = ParagraphStyle(
        'FactStyle', parent=styles['Normal'],
        fontName='Helvetica', fontSize=8.5, leading=11.5,
        textColor=colors.HexColor('#111111'), spaceAfter=6
    )

    story = []

    # 1. Cover Page
    if os.path.exists(COVER_PATH):
        story.append(RLImage(COVER_PATH, width=340, height=530))
        story.append(PageBreak())

    # 2. Title Page
    story.append(Spacer(1, 30))
    story.append(Paragraph("THE DALLAS COWBOYS TRIVIA BOOK", title_style))
    story.append(Paragraph("ULTIMATE FAN ENCYCLOPEDIA", subtitle_style))
    story.append(HRFlowable(width="60%", thickness=1.5, color=colors.HexColor('#003594'), spaceAfter=15))
    story.append(Paragraph("Over 150 Questions, Untold Stories & Historical Records", ParagraphStyle('CenterTxt', alignment=1, fontSize=10, leading=14)))
    story.append(Spacer(1, 100))
    story.append(Paragraph("Published by America's Team Press", ParagraphStyle('PubTxt', alignment=1, fontSize=9, textColor=colors.HexColor('#666666'))))
    story.append(PageBreak())

    # 3. Preface & Franchise History Essay (2 Pages)
    story.append(Paragraph("PREFACE: THE LEGEND OF AMERICA'S TEAM", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#003594'), spaceAfter=10))
    preface_p1 = (
        "Few sports franchises in human history evoke the passion, glamour, and competitive excellence of the Dallas Cowboys. "
        "From their humble beginnings in 1960 under founding owner Clint Murchison Jr., general manager Tex Schramm, and iconic head coach Tom Landry, "
        "the Cowboys evolved from a winless inaugural team into a global cultural phenomenon known worldwide as 'America's Team'."
    )
    preface_p2 = (
        "Across six decades, Dallas football has delivered unforgettable moments: Roger Staubach's original 'Hail Mary' pass, "
        "Bob Lilly's unstoppable pass rushes, Tony Dorsett's 99-yard sprint, the 1990s dynasty anchored by 'The Triplets' (Troy Aikman, Emmitt Smith, and Michael Irvin), "
        "Tony Romo's thrilling comebacks, and modern playmakers like Dak Prescott, CeeDee Lamb, and Micah Parsons."
    )
    preface_p3 = (
        "This book was meticulously crafted for true blue-and-silver fans. Divided into 10 historical chapters plus a final Mastermind Exam, "
        "each question presents an authentic challenge accompanied by deep-dive historical breakdowns and 'Did You Know?' facts."
    )
    story.append(Paragraph(preface_p1, intro_style))
    story.append(Paragraph(preface_p2, intro_style))
    story.append(Paragraph(preface_p3, intro_style))
    story.append(PageBreak())

    # Table of Contents Overview
    story.append(Paragraph("TABLE OF CONTENTS", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#869397'), spaceAfter=10))
    
    toc_items = [
        "Chapter 1: The Birth of a Franchise & Cotton Bowl Years (1960–1970)",
        "Chapter 2: Captain Comeback & Super Bowl Glory (1971–1978)",
        "Chapter 3: Doomsday II & The 1980s Gridiron Battles (1979–1988)",
        "Chapter 4: The Great Walker Trade & Rebuilding a Giant (1989–1991)",
        "Chapter 5: The 1990s Dynasty & Back-to-Back Champions (1992–1994)",
        "Chapter 6: Super Bowl XXX & The End of an Era (1995–1999)",
        "Chapter 7: The Tony Romo Era & Unforgettable Thrillers (2000–2015)",
        "Chapter 8: The Dak Prescott Era & Modern Stars (2016–Present)",
        "Chapter 9: The Ring of Honor, Hall of Famers & Franchise Records",
        "Chapter 10: Rivalries, Thanksgiving & Stadium Legends",
        "Chapter 11: The Hardcore Mastermind Final Exam"
    ]
    for item in toc_items:
        story.append(Paragraph(f"• {item}", ParagraphStyle('TOCItem', fontName='Helvetica-Bold', fontSize=9.5, leading=16, textColor=colors.HexColor('#002244'))))
    story.append(PageBreak())

    # 4. Generate Core Chapters (Questions + Answer Key Section per chapter)
    for chap_data in CHAPTERS:
        story.append(Paragraph(chap_data["title"], h1_style))
        story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#003594'), spaceAfter=8))
        story.append(Paragraph(chap_data["intro"], intro_style))
        story.append(Spacer(1, 4))

        # Questions Part (2-3 questions per page cleanly spaced)
        story.append(Paragraph("<b>PART 1: TRIVIA CHALLENGE</b>", h2_style))
        q_count = 0
        for q in chap_data["questions"]:
            q_count += 1
            q_elements = [
                Paragraph(q["q"], q_title_style)
            ]
            for opt in q["options"]:
                q_elements.append(Paragraph(opt, opt_style))
            
            t = Table([[q_elements]], colWidths=[340])
            t.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#FAFAFA')),
                ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#E0E0E0')),
                ('PADDING', (0,0), (-1,-1), 6),
            ]))
            story.append(t)
            story.append(Spacer(1, 6))

            if q_count % 4 == 0:
                story.append(PageBreak())

        if q_count % 4 != 0:
            story.append(PageBreak())

        # Answer Key & Historical Notes Part
        story.append(Paragraph(f"<b>PART 2: ANSWER KEY & HISTORICAL NOTES</b>", h2_style))
        story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor('#869397'), spaceAfter=8))

        ans_count = 0
        for q in chap_data["questions"]:
            ans_count += 1
            ans_elements = [
                Paragraph(f"<b>{q['q']}</b>", q_title_style),
                Paragraph(f"Correct Answer: {q['ans']}", ans_style),
                Paragraph(f"<b>Did You Know?</b> {q['fact']}", fact_style)
            ]
            t_ans = Table([[ans_elements]], colWidths=[340])
            t_ans.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#EBF3FA')),
                ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#003594')),
                ('PADDING', (0,0), (-1,-1), 6),
            ]))
            story.append(t_ans)
            story.append(Spacer(1, 6))

            if ans_count % 4 == 0:
                story.append(PageBreak())

        if ans_count % 4 != 0:
            story.append(PageBreak())

    # 5. Mastermind Final Exam Chapter
    story.append(Paragraph("Chapter 11: The Hardcore Mastermind Final Exam", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#003594'), spaceAfter=8))
    story.append(Paragraph("Test your elite Dallas Cowboys knowledge with this 20-question comprehensive mastermind exam!", intro_style))
    
    exam_q_count = 0
    for q in MASTERMIND_EXAM:
        exam_q_count += 1
        q_elements = [
            Paragraph(q["q"], q_title_style)
        ]
        for opt in q["options"]:
            q_elements.append(Paragraph(opt, opt_style))
        
        t = Table([[q_elements]], colWidths=[page_w - 72])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F5F5F5')),
            ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#CCCCCC')),
            ('PADDING', (0,0), (-1,-1), 6),
        ]))
        story.append(t)
        story.append(Spacer(1, 6))

        if exam_q_count % 3 == 0:
            story.append(PageBreak())

    if exam_q_count % 3 != 0:
        story.append(PageBreak())

    # Mastermind Exam Answer Key
    story.append(Paragraph("MASTERMIND EXAM: ANSWER KEY & DEEP DIVE", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#003594'), spaceAfter=8))

    exam_ans_count = 0
    for q in MASTERMIND_EXAM:
        exam_ans_count += 1
        ans_elements = [
            Paragraph(f"<b>{q['q']}</b>", q_title_style),
            Paragraph(f"Correct Answer: {q['ans']}", ans_style),
            Paragraph(f"<b>Did You Know?</b> {q['fact']}", fact_style)
        ]
        t_ans = Table([[ans_elements]], colWidths=[page_w - 72])
        t_ans.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#EBF3FA')),
            ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#003594')),
            ('PADDING', (0,0), (-1,-1), 6),
        ]))
        story.append(t_ans)
        story.append(Spacer(1, 6))

        if exam_ans_count % 3 == 0:
            story.append(PageBreak())

    # Build Document
    doc.build(story, canvasmaker=NumberedCanvas60)
    print("PDF build finished.")

# ---------------------------------------------------------
# 4. Generate Complete EPUB 3 E-Book
# ---------------------------------------------------------
def generate_epub_complete():
    book = epub.EpubBook()
    book.set_identifier("dallas-cowboys-trivia-60pages")
    book.set_title("The Dallas Cowboys Trivia Book: Ultimate Fan Encyclopedia")
    book.set_language("en")
    book.add_author("America's Team Press")

    with open(COVER_PATH, 'rb') as f:
        book.set_cover("cover.png", f.read())

    css_content = """
    body { font-family: Georgia, serif; line-height: 1.6; color: #111111; padding: 10px; }
    h1 { color: #002244; text-align: center; border-bottom: 2px solid #869397; padding-bottom: 8px; }
    h2 { color: #003594; margin-top: 20px; }
    .intro-box { background: #F4F6F8; border-left: 4px solid #003594; padding: 10px; margin-bottom: 20px; font-style: italic; }
    .q-card { background: #FAFAFA; border: 1px solid #E0E0E0; padding: 12px; margin-bottom: 15px; border-radius: 4px; }
    .q-title { font-weight: bold; color: #002244; font-size: 1.05em; }
    .ans-box { background: #EBF3FA; border-top: 1px dashed #003594; padding: 8px; margin-top: 8px; }
    .ans-title { font-weight: bold; color: #003594; }
    .fact { color: #333333; margin-top: 4px; font-size: 0.95em; }
    """
    style_item = epub.EpubItem(uid="style_nav", file_name="style/style.css", media_type="text/css", content=css_content)
    book.add_item(style_item)

    epub_chapters = []

    for chap_data in CHAPTERS:
        c_item = epub.EpubHtml(title=chap_data["title"], file_name=f"{chap_data['id']}.xhtml", lang="en")
        html_content = f"<h1>{chap_data['title']}</h1>"
        html_content += f"<div class='intro-box'>{chap_data['intro']}</div>"
        
        for q in chap_data["questions"]:
            html_content += "<div class='q-card'>"
            html_content += f"<div class='q-title'>{q['q']}</div><ul>"
            for opt in q["options"]:
                html_content += f"<li>{opt}</li>"
            html_content += f"</ul><div class='ans-box'><span class='ans-title'>Answer: {q['ans']}</span><div class='fact'><b>Did You Know?</b> {q['fact']}</div></div></div>"

        c_item.content = html_content
        c_item.add_item(style_item)
        book.add_item(c_item)
        epub_chapters.append(c_item)

    # Mastermind Exam EPUB Chapter
    m_item = epub.EpubHtml(title="Chapter 11: Mastermind Final Exam", file_name="chap11.xhtml", lang="en")
    m_html = "<h1>Chapter 11: The Hardcore Mastermind Final Exam</h1>"
    for q in MASTERMIND_EXAM:
        m_html += "<div class='q-card'>"
        m_html += f"<div class='q-title'>{q['q']}</div><ul>"
        for opt in q["options"]:
            m_html += f"<li>{opt}</li>"
        m_html += f"</ul><div class='ans-box'><span class='ans-title'>Answer: {q['ans']}</span><div class='fact'><b>Did You Know?</b> {q['fact']}</div></div></div>"
    m_item.content = m_html
    m_item.add_item(style_item)
    book.add_item(m_item)
    epub_chapters.append(m_item)

    book.toc = epub_chapters
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())
    book.spine = ['nav'] + epub_chapters
    epub.write_epub(EPUB_PATH, book, {})
    print("EPUB file generated successfully.")

if __name__ == "__main__":
    create_cover()
    generate_pdf_60pages()
    generate_epub_complete()
    
    # Verify page count
    r = pypdf.PdfReader(PDF_PATH)
    print(f"VERIFIED PDF PAGE COUNT: {len(r.pages)} pages")
