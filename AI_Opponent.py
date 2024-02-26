class PongAI:
    def __init__(self, paddle, ball, paddleHeight, paddleSpeed, screenWidth, screenHeight, difficulty=1.0):
        self.paddle = paddle  # AI's paddle, a list [x, y]
        self.ball = ball  # Reference to the ball, a list [x, y]
        self.difficulty = difficulty  # Difficulty factor, 1.0 is normal, higher is harder, lower is easier
        self.paddleHeight = paddleHeight
        self.paddleSpeed = paddleSpeed
        self.screenWidth = screenWidth
        self.screenHeight = screenHeight

    def update(self):
        # AI to move paddle based on ball position to simulate difficulty
        if self.ball[1] > self.paddle[1] + self.paddleHeight / 2 and self.ball[0] > self.screenWidth / 2:
            self.paddle[1] += self.paddleSpeed * self.difficulty
        if self.ball[1] < self.paddle[1] + self.paddleHeight / 2 and self.ball[0] > self.screenWidth / 2:
            self.paddle[1] -= self.paddleSpeed * self.difficulty

        # Prevent the AI paddle from moving out of the screen
        if self.paddle[1] < 0:
            self.paddle[1] = 0
        if self.paddle[1] > self.screenHeight - self.paddleHeight:
            self.paddle[1] = self.screenHeight - self.paddleHeight
