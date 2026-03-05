import pygame
import random
import sys

# ─────────────────────────────────────────── CONFIGURATION
SCREEN_W  = 1100
SCREEN_H  = 760
GRID_N    = 10
CS        = 48
MARGIN    = 45

LEFT_GPOS  = (MARGIN, 165)
RIGHT_GPOS = (SCREEN_W - GRID_N * CS - MARGIN, 165)
PLACE_GPOS = (150, 165)

SHIP_SIZES = [5, 4, 3, 3, 2]
SHIP_NAMES = ["Carrier (5)", "Battleship (4)", "Cruiser (3)", "Submarine (3)", "Destroyer (2)"]

BG     = (15,  25,  50)
WATER  = (25,  75, 130)
GLINE  = (55, 105, 175)
HIT_C  = (210, 55,  55)
MISS_C = (160, 160, 185)
TXT_C  = (230, 230, 255)
STAT_C = (255, 215,  90)
OK_C   = ( 80, 210,  80)
BAD_C  = (210,  80,  80)
HULL_C = (135, 138, 150)
DECK_C = ( 95,  98, 112)
BRDG_C = (165, 168, 182)
EDGE_C = ( 55,  58,  72)
BTN_N  = ( 40,  70, 120)
BTN_H  = ( 60, 100, 160)
BTN_B  = ( 70, 120, 200)
BTN_D  = ( 25,  40,  70)

pygame.init()
FONT  = pygame.font.SysFont("arial", 24)
BFONT = pygame.font.SysFont("arial", 38)
SFONT = pygame.font.SysFont("arial", 18)
QFONT = pygame.font.SysFont("arial", 21)   # question body text

# game states
MENU     = 0
P1PLACE  = 1
P2PLACE  = 2
PASS     = 3
PLAY     = 4
OVER     = 5
QUESTION = 6   # bonus-question modal

# ─────────────────────────────────────────── COLD WAR QUESTION BANK
# Texas TEKS 10th-Grade U.S. History — Cold War Unit (40 questions)
# answer = index into choices (0=A, 1=B, 2=C, 3=D)
QUESTIONS = [
    {   "q": "What U.S. foreign policy doctrine, announced in 1947, pledged support for free peoples resisting communist subjugation?",
        "choices": ["A)  Marshall Plan", "B)  Truman Doctrine", "C)  Eisenhower Doctrine", "D)  Monroe Doctrine"],
        "answer": 1 },
    {   "q": "The Marshall Plan (1948) was primarily designed to accomplish which goal?",
        "choices": ["A)  Rebuild European economies devastated by WWII", "B)  Create a military alliance against the USSR", "C)  Fund the Korean War", "D)  Establish the United Nations"],
        "answer": 0 },
    {   "q": "Which military alliance, formed in 1949, pledged collective defense among Western nations against Soviet aggression?",
        "choices": ["A)  SEATO", "B)  ANZUS Pact", "C)  NATO", "D)  The Warsaw Pact"],
        "answer": 2 },
    {   "q": "The Soviet military alliance created in 1955 in direct response to NATO was called the...",
        "choices": ["A)  COMINTERN", "B)  Warsaw Pact", "C)  Axis Alliance", "D)  Soviet Security Treaty"],
        "answer": 1 },
    {   "q": "Winston Churchill's 1946 speech warned that an 'Iron Curtain' had descended, dividing Europe between...",
        "choices": ["A)  Democracy and fascism", "B)  Capitalism and socialism only", "C)  Free nations and Soviet-dominated communist states", "D)  NATO members and neutral countries"],
        "answer": 2 },
    {   "q": "The U.S. foreign policy of 'containment' — stopping the spread of communism — was first clearly articulated by diplomat...",
        "choices": ["A)  Dean Acheson", "B)  John Foster Dulles", "C)  George Kennan", "D)  George Marshall"],
        "answer": 2 },
    {   "q": "The Berlin Airlift (1948–1949) was the U.S. and British response to which Soviet action?",
        "choices": ["A)  Construction of the Berlin Wall", "B)  The Soviet blockade of West Berlin", "C)  North Korea's invasion of South Korea", "D)  Soviet missiles placed in Cuba"],
        "answer": 1 },
    {   "q": "The Korean War began in June 1950 when which event occurred?",
        "choices": ["A)  China invaded South Korea across the Yalu River", "B)  Soviet aircraft bombed Seoul", "C)  North Korean forces crossed the 38th parallel into South Korea", "D)  The U.S. attacked a North Korean naval vessel"],
        "answer": 2 },
    {   "q": "President Truman relieved General MacArthur of command during the Korean War because MacArthur...",
        "choices": ["A)  Suffered a catastrophic military defeat at Inchon", "B)  Publicly opposed Truman's limited-war strategy and insubordination", "C)  Refused to commit troops against the Chinese army", "D)  Negotiated an unauthorized ceasefire with North Korea"],
        "answer": 1 },
    {   "q": "The Korean War concluded in 1953 with which outcome?",
        "choices": ["A)  A decisive North Korean victory", "B)  A South Korean military victory", "C)  A peace treaty that permanently unified the Korean peninsula", "D)  An armistice that restored the pre-war boundary near the 38th parallel"],
        "answer": 3 },
    {   "q": "McCarthyism, named after Senator Joseph McCarthy, is best described as a period of...",
        "choices": ["A)  U.S. diplomatic engagement with the USSR in the 1950s", "B)  Widespread accusations of communist subversion with little or no evidence", "C)  Intense U.S.-Soviet competition for dominance in space", "D)  Anti-war protests during the Vietnam War era"],
        "answer": 1 },
    {   "q": "The House Un-American Activities Committee (HUAC) became most controversial for investigating...",
        "choices": ["A)  Soviet spies working inside the Pentagon", "B)  Civil rights leaders in the American South", "C)  Suspected communist influence in Hollywood and the federal government", "D)  Vietnam War protesters on college campuses"],
        "answer": 2 },
    {   "q": "The Soviet Union launched Sputnik — the world's first artificial satellite — in which year?",
        "choices": ["A)  1953", "B)  1955", "C)  1957", "D)  1961"],
        "answer": 2 },
    {   "q": "Congress created which civilian space agency in 1958 partly in response to the Soviet Sputnik launch?",
        "choices": ["A)  DARPA", "B)  The Department of Defense Space Division", "C)  NASA", "D)  The Strategic Air Command"],
        "answer": 2 },
    {   "q": "The Cuban Missile Crisis of October 1962 began when U.S. intelligence discovered that...",
        "choices": ["A)  Cuba had secretly constructed its own nuclear bombs", "B)  Soviet ships were delivering nuclear missiles to Cuba", "C)  The Soviet Union had invaded Cuba with conventional forces", "D)  Castro was planning a nuclear attack on Miami"],
        "answer": 1 },
    {   "q": "President Kennedy's primary response during the Cuban Missile Crisis was to...",
        "choices": ["A)  Order an immediate U.S. invasion of Cuba", "B)  Launch air strikes to destroy the Soviet missile sites", "C)  Impose a naval blockade (quarantine) of Cuba to prevent Soviet ships", "D)  Request United Nations forces to remove the missiles"],
        "answer": 2 },
    {   "q": "The failed April 1961 CIA-sponsored invasion of Cuba by U.S.-trained Cuban exiles is known as...",
        "choices": ["A)  Operation Mongoose", "B)  The Bay of Pigs invasion", "C)  Operation Neptune Spear", "D)  The Cuba Liberation Campaign"],
        "answer": 1 },
    {   "q": "The Berlin Wall, built to stop East Germans from fleeing to the West, was constructed in which year?",
        "choices": ["A)  1949", "B)  1955", "C)  1961", "D)  1968"],
        "answer": 2 },
    {   "q": "In his January 1961 farewell address, President Eisenhower's most famous warning concerned the dangers of the...",
        "choices": ["A)  Soviet nuclear arsenal and missile gap", "B)  Military-industrial complex", "C)  Communist Party's influence in U.S. labor unions", "D)  Domino effect spreading communism in Southeast Asia"],
        "answer": 1 },
    {   "q": "The 'domino theory,' used to justify U.S. involvement in Vietnam, argued that...",
        "choices": ["A)  Nuclear weapons technology would inevitably spread across all Asian nations", "B)  U.S. economic aid alone could prevent communism from spreading", "C)  If one country fell to communism, neighboring countries would soon follow", "D)  The U.S. should immediately withdraw all military forces from Asia"],
        "answer": 2 },
    {   "q": "NSC-68, the top-secret 1950 U.S. government policy paper, recommended that America respond to Soviet power by...",
        "choices": ["A)  Seeking direct diplomatic negotiations with Stalin", "B)  Withdrawing U.S. forces from Western Europe", "C)  Massively increasing U.S. defense spending", "D)  Reducing the nuclear arsenal to show good faith"],
        "answer": 2 },
    {   "q": "The Cold War nuclear doctrine of Mutually Assured Destruction (MAD) meant that...",
        "choices": ["A)  Only the United States had sufficient nuclear force to destroy the Soviet Union", "B)  Any nuclear first strike would result in the total destruction of both superpowers, deterring attack", "C)  Conventional military forces, not nuclear weapons, would decide any Cold War conflict", "D)  A nuclear war between the superpowers was statistically inevitable by 1970"],
        "answer": 1 },
    {   "q": "The foreign policy of détente, pursued in the 1970s by Nixon and Kissinger, refers to...",
        "choices": ["A)  A major increase in U.S. military spending to surpass the Soviets", "B)  A relaxation of Cold War tensions and improved diplomatic relations with the Soviet Union", "C)  The U.S. strategy of withdrawing all forces from Southeast Asia", "D)  Reagan's policy of confronting Soviet expansionism worldwide"],
        "answer": 1 },
    {   "q": "President Nixon's historic 1972 visit to China was significant in Cold War diplomacy because it...",
        "choices": ["A)  Led to China becoming a member of NATO", "B)  Created a formal U.S.-China military alliance against Japan", "C)  Restored diplomatic relations and exploited tensions between China and the Soviet Union", "D)  Directly ended U.S. military involvement in the Vietnam War"],
        "answer": 2 },
    {   "q": "The Gulf of Tonkin Resolution (1964) was significant because it gave President Johnson...",
        "choices": ["A)  Authority to use nuclear weapons against North Vietnam if attacked", "B)  Broad power to escalate U.S. military involvement in Vietnam without a formal declaration of war", "C)  Congressional permission to invade Cuba and remove Castro", "D)  The legal authority to reinstate the military draft"],
        "answer": 1 },
    {   "q": "The Ho Chi Minh Trail, critical to North Vietnam's war effort, was primarily...",
        "choices": ["A)  A North Vietnamese supply network through Laos and Cambodia into South Vietnam", "B)  A U.S. military strategy for destroying North Vietnamese infrastructure", "C)  A peace agreement signed between North and South Vietnam in 1968", "D)  A trade route linking China to ports in South Vietnam"],
        "answer": 0 },
    {   "q": "President Nixon's strategy of 'Vietnamization' was designed to...",
        "choices": ["A)  Deploy additional U.S. ground combat troops to decisively win the war", "B)  Intensify the bombing of North Vietnam until it surrendered", "C)  Gradually withdraw U.S. troops while strengthening South Vietnamese forces to fight alone", "D)  Negotiate a direct peace settlement with the Viet Cong leadership"],
        "answer": 2 },
    {   "q": "The Strategic Arms Limitation Talks (SALT I, 1972) between the U.S. and USSR produced an agreement that...",
        "choices": ["A)  Required complete nuclear disarmament by both superpowers within ten years", "B)  Placed limits on certain categories of nuclear weapons and delivery systems", "C)  Established a mutual defense treaty between the two nations", "D)  Permanently ended the arms race and the Cold War"],
        "answer": 1 },
    {   "q": "The Reagan Doctrine of the 1980s is best described as a U.S. policy of...",
        "choices": ["A)  Seeking to renew détente and cooperative relations with the Soviet Union", "B)  Providing military and economic support to anti-communist movements fighting Soviet-backed governments", "C)  Constructing a space-based missile defense shield over North America", "D)  Withdrawing U.S. military forces from overseas commitments in Europe and Asia"],
        "answer": 1 },
    {   "q": "President Reagan's proposed missile defense system, popularly nicknamed 'Star Wars,' was officially called the...",
        "choices": ["A)  Strategic Arms Limitation Treaty (SALT II)", "B)  Nuclear Freeze Initiative", "C)  Strategic Defense Initiative (SDI)", "D)  Intermediate-Range Nuclear Forces Treaty"],
        "answer": 2 },
    {   "q": "The fall of the Berlin Wall in November 1989 is best interpreted as a symbol of...",
        "choices": ["A)  The beginning of a new Cold War between the superpowers", "B)  A decisive U.S. military victory over the Soviet Union in Europe", "C)  The collapse of communist governments across Eastern Europe and the end of the Cold War", "D)  German reunification achieved with active Soviet support"],
        "answer": 2 },
    {   "q": "Julius and Ethel Rosenberg were tried and executed in 1953 after being convicted of...",
        "choices": ["A)  Plotting to assassinate President Truman and Vice President Barkley", "B)  Organizing illegal anti-government protests during the Korean War", "C)  Passing classified U.S. nuclear weapons secrets to the Soviet Union", "D)  Committing treason by publicly burning their draft cards"],
        "answer": 2 },
    {   "q": "Secretary of State John Foster Dulles's doctrine of 'massive retaliation' threatened that any Soviet aggression would be answered with...",
        "choices": ["A)  An immediate and overwhelming conventional military counterattack", "B)  Strict economic sanctions and a full trade embargo on the USSR", "C)  A U.S. nuclear strike at a time and place of America's choosing", "D)  Complete diplomatic isolation of the Soviet Union by Western allies"],
        "answer": 2 },
    {   "q": "U.S. military action in Korea was unusual in American history because it was authorized by...",
        "choices": ["A)  A formal declaration of war voted on by the U.S. Congress", "B)  A United Nations Security Council resolution calling for member states to repel the invasion", "C)  A secret executive order signed by President Truman without congressional knowledge", "D)  A NATO collective defense vote requiring all member nations to contribute troops"],
        "answer": 1 },
    {   "q": "The Cold War strategy of 'brinkmanship,' associated with Secretary Dulles, involved...",
        "choices": ["A)  Offering economic incentives to persuade communist nations to switch sides", "B)  Quietly backing away from dangerous confrontations to preserve peace", "C)  Pushing a dangerous confrontation to the very edge of war to force the enemy to back down first", "D)  Using nuclear disarmament agreements as a tool of Cold War diplomacy"],
        "answer": 2 },
    {   "q": "The Helsinki Accords of 1975 were historically significant because they...",
        "choices": ["A)  Formally ended U.S. military involvement in the Vietnam War", "B)  Recognized post-World War II European borders and included human rights provisions", "C)  Created the political framework that became the European Union", "D)  Established the world's first international nuclear test ban treaty"],
        "answer": 1 },
    {   "q": "The United States achieved the final goal of the Space Race when NASA's Apollo 11 mission landed on the Moon in...",
        "choices": ["A)  1965", "B)  1967", "C)  1969", "D)  1972"],
        "answer": 2 },
    {   "q": "A 'proxy war' in Cold War terminology describes a conflict where...",
        "choices": ["A)  U.S. and Soviet troops fought each other directly in a third country", "B)  The U.S. and USSR supported opposing sides in regional conflicts to advance their interests without direct combat", "C)  Two Cold War allies fought each other while the superpowers stayed neutral", "D)  Nuclear weapons were placed in a third country by one of the superpowers"],
        "answer": 1 },
    {   "q": "State Department official Alger Hiss became a symbol of Red Scare fears because he was...",
        "choices": ["A)  The Senate Republican who first accused Communists of infiltrating the Army", "B)  Convicted of perjury related to accusations that he had spied for the Soviet Union, stoking fears of communist infiltration", "C)  A Soviet KGB officer who personally recruited American nuclear scientists as spies", "D)  The founder of the House Un-American Activities Committee"],
        "answer": 1 },
    {   "q": "Kennedy's policy of 'flexible response' — which replaced Eisenhower's massive retaliation — meant the U.S. would...",
        "choices": ["A)  Always respond to Soviet aggression with an immediate nuclear strike", "B)  Match the scale of any Soviet military threat with a proportional response, conventional or nuclear", "C)  Avoid any military confrontation with the Soviets to prevent escalation", "D)  Rely entirely on economic sanctions rather than military force"],
        "answer": 1 },
    {   "q": "Fighting the Korean War to restore the pre-war border rather than to conquer North Korea reflected the Cold War doctrine of...",
        "choices": ["A)  Massive Retaliation", "B)  Brinkmanship", "C)  Rollback", "D)  Containment"],
        "answer": 3 },
]


# ─────────────────────────────────────────── GRID
class Grid:
    def __init__(self, auto=True):
        self.cells = [["~"] * GRID_N for _ in range(GRID_N)]
        self.ships = []
        if auto:
            for s in SHIP_SIZES:
                self._rand(s)

    def _rand(self, size):
        while True:
            o = random.choice(["H", "V"])
            r = random.randint(0, GRID_N - (1 if o == "H" else size))
            c = random.randint(0, GRID_N - (size if o == "H" else 1))
            if self.can_place(r, c, size, o):
                self.do_place(r, c, size, o)
                return

    def can_place(self, row, col, size, orient):
        for i in range(size):
            r = row + (i if orient == "V" else 0)
            c = col + (i if orient == "H" else 0)
            if not (0 <= r < GRID_N and 0 <= c < GRID_N):
                return False
            if self.cells[r][c] != "~":
                return False
        return True

    def do_place(self, row, col, size, orient):
        for i in range(size):
            r = row + (i if orient == "V" else 0)
            c = col + (i if orient == "H" else 0)
            self.cells[r][c] = "S"
        self.ships.append({"row": row, "col": col, "size": size, "orientation": orient})

    def clear(self):
        self.cells = [["~"] * GRID_N for _ in range(GRID_N)]
        self.ships.clear()

    def randomize(self):
        self.clear()
        for s in SHIP_SIZES:
            self._rand(s)

    def attack(self, row, col):
        v = self.cells[row][col]
        if   v == "S": self.cells[row][col] = "H"; return "hit"
        elif v == "~": self.cells[row][col] = "M"; return "miss"
        return "already"

    def all_sunk(self):
        return all(v != "S" for row in self.cells for v in row)


# ─────────────────────────────────────────── GAME
class BattleshipGame:

    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
        pygame.display.set_caption("Battleship")
        self.clock  = pygame.time.Clock()
        self._build_ui()
        self.new_game()

    # ── reset ─────────────────────────────────────────────────────────────────
    def new_game(self):
        self.state      = MENU
        self.two_player = False
        self.grid_p1    = None
        self.grid_p2    = None
        self.pl_ships   = []
        self.pl_orient  = "H"
        self.cur_player = 1
        self.status     = ""
        self.ai_delay   = 0
        self.pass_msg   = ""
        self.pass_next  = None
        # question state
        self.q_pool     = list(range(len(QUESTIONS)))   # indices not yet drawn
        self.active_q   = None     # current question dict
        self.q_answer   = -1       # player's choice index; -1 = not yet answered
        self.score_p1   = 0        # bonus turns earned by player 1
        self.score_p2   = 0        # bonus turns earned by player 2 / AI (1P shows player score only)

    def _build_ui(self):
        cx = SCREEN_W // 2
        # menu
        self.b_1p  = pygame.Rect(cx - 165, 340, 150, 55)
        self.b_2p  = pygame.Rect(cx +  15, 340, 150, 55)
        # placement panel
        self.b_rot = pygame.Rect(715, 430, 160, 45)
        self.b_rnd = pygame.Rect(715, 490, 160, 45)
        self.b_ok  = pygame.Rect(715, 560, 160, 45)
        # HUD controls — top-right corner, visible during all gameplay states
        self.b_reset = pygame.Rect(862, 10, 108, 34)
        self.b_quit  = pygame.Rect(980, 10, 108, 34)
        # question modal — panel and 4 answer buttons + continue
        self.q_panel = pygame.Rect(175, 68, 750, 638)
        self.q_btns  = [pygame.Rect(200, 355 + i * 68, 700, 55) for i in range(4)]
        self.q_cont  = pygame.Rect(400, 650, 300, 45)

    # ── placement helpers ─────────────────────────────────────────────────────
    def _setup_placement(self, player):
        if player == 1:
            self.grid_p1 = Grid(auto=False)
        else:
            self.grid_p2 = Grid(auto=False)
        self.pl_ships  = list(SHIP_SIZES)
        self.pl_orient = "H"

    def _placement_grid(self):
        return self.grid_p1 if self.state == P1PLACE else self.grid_p2

    def _placement_hover(self, mx, my):
        x0, y0 = PLACE_GPOS
        if x0 <= mx < x0 + GRID_N * CS and y0 <= my < y0 + GRID_N * CS:
            return (my - y0) // CS, (mx - x0) // CS
        return None

    def _confirm_placement(self):
        if self.state == P1PLACE:
            if self.two_player:
                self._setup_placement(2)
                self.pass_msg  = "Hand the device to  Player 2\n\nPlayer 2 — place your fleet!"
                self.pass_next = P2PLACE
                self.state     = PASS
            else:
                self.grid_p2 = Grid(auto=True)
                self.cur_player = 1
                self.status = "Your turn — click the enemy grid to fire!"
                self.state  = PLAY
        else:
            self.cur_player = 1
            self.status     = "Player 1's turn — click the enemy grid!"
            self.pass_msg   = "Hand the device back to  Player 1\n\nThe battle begins!"
            self.pass_next  = PLAY
            self.state      = PASS

    # ── play helpers ──────────────────────────────────────────────────────────
    def _atk_grid(self): return self.grid_p1 if self.cur_player == 1 else self.grid_p2
    def _def_grid(self): return self.grid_p2 if self.cur_player == 1 else self.grid_p1

    def _cell_at(self, mpos, gpos):
        x0, y0 = gpos
        mx, my = mpos
        if x0 <= mx < x0 + GRID_N * CS and y0 <= my < y0 + GRID_N * CS:
            return (my - y0) // CS, (mx - x0) // CS
        return None

    def _pass_to_next(self):
        nxt = 3 - self.cur_player
        self.cur_player = nxt
        self.status     = f"Player {nxt}'s turn — click the enemy grid!"
        self.pass_msg   = f"Hand the device to  Player {nxt}\n\nPlayer {nxt} — it's your turn!"
        self.pass_next  = PLAY
        self.state      = PASS

    # ── AI ────────────────────────────────────────────────────────────────────
    def _ai_turn(self):
        while True:
            r = random.randint(0, GRID_N - 1)
            c = random.randint(0, GRID_N - 1)
            res = self.grid_p1.attack(r, c)
            if res != "already":
                word = "hit" if res == "hit" else "missed"
                self.status = f"AI {word}!  Your turn."
                return

    # ── question helpers ──────────────────────────────────────────────────────
    def _start_question(self):
        """Pick a random unused question and switch to QUESTION state."""
        if not self.q_pool:
            self.q_pool = list(range(len(QUESTIONS)))   # refill when exhausted
        idx = random.choice(self.q_pool)
        self.q_pool.remove(idx)
        self.active_q = QUESTIONS[idx]
        self.q_answer = -1
        self.state    = QUESTION

    def _resolve_question(self):
        """Called when the player clicks Continue after answering."""
        correct = (self.q_answer == self.active_q["answer"])
        if correct:
            # Award bonus turn — same player fires again (no turn switch / pass)
            if self.cur_player == 1:
                self.score_p1 += 1
            else:
                self.score_p2 += 1
            who = "You earn" if not self.two_player else f"Player {self.cur_player} earns"
            self.status = f"Correct! {who} a BONUS TURN!"
            self.state  = PLAY
        else:
            # Wrong — normal turn advance
            self.status = "Incorrect. Switch turns."
            if self.two_player:
                self._pass_to_next()        # sets state = PASS
            else:
                self.cur_player = 2
                self.ai_delay   = 0
                self.state      = PLAY

    # ── text wrap helper ──────────────────────────────────────────────────────
    def _wrap(self, text, font, max_w):
        words = text.split()
        lines, line = [], ""
        for w in words:
            test = (line + " " + w).strip()
            if font.size(test)[0] <= max_w:
                line = test
            else:
                if line:
                    lines.append(line)
                line = w
        if line:
            lines.append(line)
        return lines

    # ── drawing ───────────────────────────────────────────────────────────────
    def _txt(self, text, font, x, y, color=TXT_C):
        self.screen.blit(font.render(text, True, color), (x, y))

    def _btn(self, rect, label, active=True):
        mx, my = pygame.mouse.get_pos()
        hov = rect.collidepoint(mx, my) and active
        pygame.draw.rect(self.screen, BTN_H if hov else (BTN_N if active else BTN_D), rect, border_radius=8)
        pygame.draw.rect(self.screen, BTN_B if hov else (50, 90, 160), rect, 2, border_radius=8)
        s = FONT.render(label, True, TXT_C if active else (100, 100, 130))
        self.screen.blit(s, (rect.centerx - s.get_width() // 2, rect.centery - s.get_height() // 2))

    def _draw_ship(self, ship, gpos):
        x0, y0 = gpos
        r, c, sz, o = ship["row"], ship["col"], ship["size"], ship["orientation"]
        pad = 4
        rx = x0 + c * CS + pad
        ry = y0 + r * CS + pad
        rw = sz * CS - pad * 2 if o == "H" else CS - pad * 2
        rh = CS - pad * 2      if o == "H" else sz * CS - pad * 2
        hull = pygame.Rect(rx, ry, rw, rh)
        pygame.draw.rect(self.screen, HULL_C, hull, border_radius=6)
        if o == "H":
            pygame.draw.rect(self.screen, DECK_C, pygame.Rect(rx+4, ry+rh//4, rw-8, rh//2), border_radius=4)
            bw, bh = max(10, rw//4), max(6, rh-10)
            bx, by = rx + rw//2 - bw//2, ry + 5
        else:
            pygame.draw.rect(self.screen, DECK_C, pygame.Rect(rx+rw//4, ry+4, rw//2, rh-8), border_radius=4)
            bw, bh = max(6, rw-10), max(10, rh//4)
            bx, by = rx + 5, ry + rh//2 - bh//2
        pygame.draw.rect(self.screen, BRDG_C, pygame.Rect(bx, by, bw, bh), border_radius=3)
        pygame.draw.rect(self.screen, EDGE_C, hull, 2, border_radius=6)

    def _draw_grid(self, grid, gpos, hide_ships=False, preview=None):
        x0, y0 = gpos
        pygame.draw.rect(self.screen, WATER, (x0, y0, GRID_N * CS, GRID_N * CS))
        if not hide_ships:
            for ship in grid.ships:
                self._draw_ship(ship, gpos)
        for row in range(GRID_N):
            for col in range(GRID_N):
                rect = pygame.Rect(x0 + col * CS, y0 + row * CS, CS, CS)
                cell = grid.cells[row][col]
                if cell == "H":
                    pygame.draw.rect(self.screen, HIT_C, rect.inflate(-8, -8), border_radius=4)
                    cx_, cy_ = rect.center
                    pygame.draw.line(self.screen, (255, 200, 0), (cx_-8, cy_-8), (cx_+8, cy_+8), 3)
                    pygame.draw.line(self.screen, (255, 200, 0), (cx_+8, cy_-8), (cx_-8, cy_+8), 3)
                elif cell == "M":
                    pygame.draw.circle(self.screen, MISS_C, rect.center, 8)
                    pygame.draw.circle(self.screen, (100, 100, 120), rect.center, 8, 2)
        if preview:
            pr, pc, psz, po, valid = preview
            col_p = OK_C if valid else BAD_C
            for i in range(psz):
                r = pr + (i if po == "V" else 0)
                c = pc + (i if po == "H" else 0)
                if 0 <= r < GRID_N and 0 <= c < GRID_N:
                    prect = pygame.Rect(x0 + c*CS + 3, y0 + r*CS + 3, CS - 6, CS - 6)
                    pygame.draw.rect(self.screen, col_p, prect, border_radius=4)
                    pygame.draw.rect(self.screen, (255, 255, 255), prect, 1, border_radius=4)
        for row in range(GRID_N):
            for col in range(GRID_N):
                pygame.draw.rect(self.screen, GLINE, (x0 + col*CS, y0 + row*CS, CS, CS), 1)
        for col in range(GRID_N):
            s = SFONT.render(chr(ord("A") + col), True, TXT_C)
            self.screen.blit(s, (x0 + col*CS + CS//2 - s.get_width()//2, y0 - 20))
        for row in range(GRID_N):
            s = SFONT.render(str(row + 1), True, TXT_C)
            self.screen.blit(s, (x0 - 24, y0 + row*CS + CS//2 - s.get_height()//2))

    # ── HUD buttons ───────────────────────────────────────────────────────────
    def _draw_hud_buttons(self):
        """Reset and Quit buttons fixed in the top-right corner."""
        mx, my = pygame.mouse.get_pos()
        for rect, label, base_c, hov_c, brd_c in [
            (self.b_reset, "Reset", (38, 62, 105), (58, 92, 148), (80, 130, 200)),
            (self.b_quit,  "Quit",  (90, 28, 28),  (130, 44, 44), (190, 65, 65)),
        ]:
            hov = rect.collidepoint(mx, my)
            pygame.draw.rect(self.screen, hov_c if hov else base_c, rect, border_radius=6)
            pygame.draw.rect(self.screen, brd_c, rect, 2, border_radius=6)
            s = SFONT.render(label, True, TXT_C)
            self.screen.blit(s, (rect.centerx - s.get_width()//2,
                                 rect.centery - s.get_height()//2))

    # ── screens ───────────────────────────────────────────────────────────────
    def _draw_menu(self):
        self.screen.fill(BG)
        cx = SCREEN_W // 2
        s = BFONT.render("BATTLESHIP", True, TXT_C)
        self.screen.blit(s, (cx - s.get_width()//2, 70))
        s = FONT.render("Select game mode", True, (170, 190, 220))
        self.screen.blit(s, (cx - s.get_width()//2, 250))
        self._btn(self.b_1p, "1 Player")
        self._btn(self.b_2p, "2 Players")
        notes = [
            "1 Player — you vs. the AI",
            "2 Players — hot-seat on the same screen",
            "",
            "Hit an enemy ship → answer a Cold War question.",
            "Correct answer = BONUS TURN!",
            "",
            "Place ships manually or click Randomize.",
            "Press R to flip ship orientation.",
        ]
        y = 420
        for line in notes:
            col = STAT_C if "BONUS" in line else (160, 180, 210)
            s = SFONT.render(line, True, col)
            self.screen.blit(s, (cx - s.get_width()//2, y))
            y += 26

    def _draw_placement(self):
        g      = self._placement_grid()
        who    = "Player 1" if self.state == P1PLACE else "Player 2"
        mx, my = pygame.mouse.get_pos()
        hover  = self._placement_hover(mx, my)
        preview = None
        if hover and self.pl_ships:
            r, c  = hover
            sz    = self.pl_ships[0]
            valid = g.can_place(r, c, sz, self.pl_orient)
            preview = (r, c, sz, self.pl_orient, valid)

        self.screen.fill(BG)
        title = f"{who} — Place Your Fleet"
        ts = BFONT.render(title, True, TXT_C)
        self.screen.blit(ts, (SCREEN_W//2 - ts.get_width()//2, 40))
        self._draw_grid(g, PLACE_GPOS, preview=preview)

        px = 715
        self._txt("Your Fleet", FONT, px, 170, STAT_C)
        num_placed = len(SHIP_SIZES) - len(self.pl_ships)
        for i, name in enumerate(SHIP_NAMES):
            if i < num_placed:
                col, pre = OK_C,  "✓"
            elif i == num_placed:
                col, pre = STAT_C, "▶"
            else:
                col, pre = (150, 150, 170), "  "
            self._txt(f"{pre}  {name}", SFONT, px, 210 + i * 35, col)

        self._txt("─" * 22, SFONT, px, 393, (70, 90, 130))
        dir_txt = "Direction:  →  Horizontal" if self.pl_orient == "H" else "Direction:  ↓  Vertical"
        self._txt(dir_txt, SFONT, px, 410, (180, 200, 230))
        self._btn(self.b_rot, "Rotate  (R)")
        self._btn(self.b_rnd, "Randomize")
        self._btn(self.b_ok,  "Confirm  →", active=not self.pl_ships)

        if self.pl_ships:
            hint = f"Placing:  {SHIP_NAMES[num_placed]}  |  {'Horizontal' if self.pl_orient == 'H' else 'Vertical'}"
        else:
            hint = "All ships placed — click  Confirm →  to continue!"
        hs = SFONT.render(hint, True, STAT_C)
        self.screen.blit(hs, (SCREEN_W//2 - hs.get_width()//2, SCREEN_H - 38))

    def _draw_pass(self):
        self.screen.fill(BG)
        lines = self.pass_msg.split("\n")
        y = SCREEN_H // 2 - len(lines) * 30
        for line in lines:
            if line.strip():
                s = BFONT.render(line.strip(), True, TXT_C)
                self.screen.blit(s, (SCREEN_W//2 - s.get_width()//2, y))
                y += BFONT.get_height() + 10
            else:
                y += 20
        hint = FONT.render("Click anywhere to continue…", True, STAT_C)
        self.screen.blit(hint, (SCREEN_W//2 - hint.get_width()//2, SCREEN_H - 80))
        self._draw_hud_buttons()

    def _draw_play(self):
        self.screen.fill(BG)
        if self.two_player:
            l_grid, r_grid = self._atk_grid(), self._def_grid()
            l_lbl = f"Player {self.cur_player}'s Fleet"
            r_lbl = f"Player {3 - self.cur_player}'s Fleet"
        else:
            l_grid, r_grid = self.grid_p1, self.grid_p2
            l_lbl, r_lbl   = "Your Fleet", "Enemy Fleet"

        self._txt(l_lbl, BFONT, LEFT_GPOS[0],  110)
        self._txt(r_lbl, BFONT, RIGHT_GPOS[0], 110)
        self._draw_grid(l_grid, LEFT_GPOS)
        self._draw_grid(r_grid, RIGHT_GPOS, hide_ships=True)

        # score display
        if self.two_player:
            sc1 = SFONT.render(f"P1 Bonus Turns: {self.score_p1}", True, STAT_C)
            sc2 = SFONT.render(f"P2 Bonus Turns: {self.score_p2}", True, STAT_C)
            self.screen.blit(sc1, (LEFT_GPOS[0], SCREEN_H - 72))
            self.screen.blit(sc2, (RIGHT_GPOS[0], SCREEN_H - 72))
        else:
            sc = SFONT.render(f"Bonus Turns Earned: {self.score_p1}", True, STAT_C)
            self.screen.blit(sc, (SCREEN_W//2 - sc.get_width()//2, SCREEN_H - 72))

        s = FONT.render(self.status, True, STAT_C)
        self.screen.blit(s, (SCREEN_W//2 - s.get_width()//2, SCREEN_H - 46))

        if self.state == OVER:
            if self.two_player:
                winner = f"Player {self.cur_player} Wins!"
            else:
                winner = "You Win!" if self.grid_p2.all_sunk() else "AI Wins!"
            banner = winner + "  Click to play again."
            bs = BFONT.render(banner, True, (100, 255, 150))
            bx = SCREEN_W//2 - bs.get_width()//2 - 14
            by = SCREEN_H//2 - bs.get_height()//2 - 14
            pygame.draw.rect(self.screen, (10, 20, 40),
                             (bx, by, bs.get_width()+28, bs.get_height()+28), border_radius=10)
            pygame.draw.rect(self.screen, (100, 255, 150),
                             (bx, by, bs.get_width()+28, bs.get_height()+28), 2, border_radius=10)
            self.screen.blit(bs, (bx + 14, by + 14))
        self._draw_hud_buttons()

    def _draw_question(self):
        """Draw the Cold War bonus-question modal over a dimmed play screen."""
        # dim background
        self._draw_play()
        dim = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        dim.fill((0, 0, 0, 170))
        self.screen.blit(dim, (0, 0))

        q   = self.active_q
        p   = self.q_panel
        mx  = pygame.mouse.get_pos()[0]

        # panel background
        pygame.draw.rect(self.screen, (18, 32, 65), p, border_radius=14)
        pygame.draw.rect(self.screen, STAT_C, p, 2, border_radius=14)

        # header
        hdr = BFONT.render("★  BONUS QUESTION  ★", True, STAT_C)
        self.screen.blit(hdr, (p.centerx - hdr.get_width()//2, p.top + 18))

        sub = SFONT.render("Answer correctly to earn a BONUS TURN!", True, (180, 200, 240))
        self.screen.blit(sub, (p.centerx - sub.get_width()//2, p.top + 68))

        pygame.draw.line(self.screen, (50, 80, 140),
                         (p.left + 20, p.top + 100), (p.right - 20, p.top + 100), 1)

        # question text (wrapped)
        lines = self._wrap(q["q"], QFONT, p.width - 60)
        ty = p.top + 115
        for line in lines:
            ls = QFONT.render(line, True, TXT_C)
            self.screen.blit(ls, (p.left + 30, ty))
            ty += QFONT.get_height() + 6

        # answer buttons
        answered = self.q_answer != -1
        for i, (btn, choice) in enumerate(zip(self.q_btns, q["choices"])):
            if answered:
                if   i == q["answer"]:         fill = (30, 120, 50)
                elif i == self.q_answer:       fill = (120, 30, 30)
                else:                          fill = (25, 42, 80)
                border = OK_C if i == q["answer"] else (BAD_C if i == self.q_answer else (40, 60, 100))
            else:
                hov   = btn.collidepoint(pygame.mouse.get_pos())
                fill   = BTN_H if hov else BTN_N
                border = BTN_B
            pygame.draw.rect(self.screen, fill,   btn, border_radius=8)
            pygame.draw.rect(self.screen, border, btn, 2, border_radius=8)
            cs = QFONT.render(choice, True, TXT_C)
            self.screen.blit(cs, (btn.left + 18, btn.centery - cs.get_height()//2))

        # after answering: show explanation + continue button
        if answered:
            correct = self.q_answer == q["answer"]
            fb_txt  = "✓ Correct!  You earn a BONUS TURN!" if correct else "✗ Incorrect.  No bonus this time."
            fb_col  = OK_C if correct else BAD_C
            fb_s    = FONT.render(fb_txt, True, fb_col)
            self.screen.blit(fb_s, (p.centerx - fb_s.get_width()//2, self.q_cont.top - 38))
            self._btn(self.q_cont, "Continue  →")
        self._draw_hud_buttons()

    # ── main loop ─────────────────────────────────────────────────────────────
    def run(self):
        while True:
            dt    = self.clock.tick(60)
            mx,my = pygame.mouse.get_pos()
            mpos  = (mx, my)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); sys.exit()

                # ── GLOBAL HUD: Reset / Quit (all states except menus)
                if (event.type == pygame.MOUSEBUTTONDOWN
                        and self.state not in (MENU, P1PLACE, P2PLACE)):
                    if self.b_reset.collidepoint(mpos):
                        self.new_game()
                        continue          # skip state-specific handlers this event
                    elif self.b_quit.collidepoint(mpos):
                        pygame.quit(); sys.exit()

                # ── MENU
                if self.state == MENU:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if self.b_1p.collidepoint(mpos):
                            self.two_player = False
                            self._setup_placement(1)
                            self.state = P1PLACE
                        elif self.b_2p.collidepoint(mpos):
                            self.two_player = True
                            self._setup_placement(1)
                            self.state = P1PLACE

                # ── PLACEMENT
                elif self.state in (P1PLACE, P2PLACE):
                    g = self._placement_grid()
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                        self.pl_orient = "V" if self.pl_orient == "H" else "H"
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if self.b_rot.collidepoint(mpos):
                            self.pl_orient = "V" if self.pl_orient == "H" else "H"
                        elif self.b_rnd.collidepoint(mpos):
                            g.randomize()
                            self.pl_ships = []
                        elif self.b_ok.collidepoint(mpos) and not self.pl_ships:
                            self._confirm_placement()
                        else:
                            hover = self._placement_hover(mx, my)
                            if hover and self.pl_ships:
                                r, c = hover
                                sz   = self.pl_ships[0]
                                if g.can_place(r, c, sz, self.pl_orient):
                                    g.do_place(r, c, sz, self.pl_orient)
                                    self.pl_ships.pop(0)

                # ── PASS SCREEN
                elif self.state == PASS:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        self.state = self.pass_next

                # ── PLAY
                elif self.state == PLAY:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if self.two_player or self.cur_player == 1:
                            cell = self._cell_at(mpos, RIGHT_GPOS)
                            if cell:
                                r, c = cell
                                res  = self._def_grid().attack(r, c)
                                if res == "hit":
                                    if self._def_grid().all_sunk():
                                        # Win — no question needed
                                        self.state = OVER
                                        if self.two_player:
                                            self.status = f"Player {self.cur_player} sank all ships!"
                                        else:
                                            self.status = "You sank all enemy ships!"
                                    else:
                                        # Hit but game continues → show question
                                        if self.two_player:
                                            self.status = f"Player {self.cur_player} hit! Answer to earn a bonus turn."
                                        else:
                                            self.status = "Hit! Answer correctly for a bonus turn."
                                        self._start_question()
                                elif res == "miss":
                                    if self.two_player:
                                        self.status = f"Player {self.cur_player} missed."
                                    else:
                                        self.status = "Missed.  AI thinking…"
                                    # Switch turns immediately on a miss (no question)
                                    if self.two_player:
                                        self._pass_to_next()
                                    else:
                                        self.cur_player = 2
                                        self.ai_delay   = 0

                # ── QUESTION MODAL
                elif self.state == QUESTION:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if self.q_answer == -1:
                            # Choose an answer
                            for i, btn in enumerate(self.q_btns):
                                if btn.collidepoint(mpos):
                                    self.q_answer = i
                                    break
                        else:
                            # Continue button
                            if self.q_cont.collidepoint(mpos):
                                self._resolve_question()

                # ── GAME OVER
                elif self.state == OVER:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        self.new_game()

            # non-blocking AI delay (1-player only, AI never gets questions)
            if self.state == PLAY and not self.two_player and self.cur_player == 2:
                self.ai_delay += dt
                if self.ai_delay >= 600:
                    self._ai_turn()
                    if self.grid_p1.all_sunk():
                        self.state  = OVER
                        self.status = "All your ships sunk — AI Wins!"
                    self.cur_player = 1

            # render
            if   self.state == MENU:                  self._draw_menu()
            elif self.state in (P1PLACE, P2PLACE):    self._draw_placement()
            elif self.state == PASS:                   self._draw_pass()
            elif self.state in (PLAY, OVER):           self._draw_play()
            elif self.state == QUESTION:               self._draw_question()

            pygame.display.flip()


if __name__ == "__main__":
    game = BattleshipGame()
    game.run()
