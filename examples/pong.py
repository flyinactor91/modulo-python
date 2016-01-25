#!/usr/local/bin/python

import modulo
import time
import math

lastUpdateTime = time.time()


class Pong :

    def __init__(self) :
        self._port = modulo.Port()
        self._display = modulo.Display(self._port)
        self._knob = modulo.Knob(self._port)

        self._width = self._display.width
        self._height = self._display.height
        self._paddleWidth = 3
        self._paddleHeight = 10

        self._leftPaddlePos = self._height/2
        self._rightPaddlePos = self._height/2
        self._knobPos = self._knob.getPosition()

        self._paused = True
        self._lastUpdateTime = time.time()
        self._ballX = 10
        self._ballY = self._height/2

        self._ballSpeed = 80
        self._ballDx = .9
        self._ballDy = .1

        self._leftPaddleSpeed = self._ballSpeed*.9

        self._rightScore = 0
        self._leftScore = 0

    def update_input(self) :
        newKnobPos = self._knob.getPosition()
        self._rightPaddlePos += 5*(newKnobPos - self._knobPos)
        self._knobPos = newKnobPos

        minPaddlePosition = self._paddleHeight/2
        maxPaddlePosition = self._height-self._paddleHeight/2

        self._rightPaddlePos = max(self._rightPaddlePos, minPaddlePosition)
        self._rightPaddlePos = min(self._rightPaddlePos, maxPaddlePosition)

    def end_round(self) :
        self.draw()

        # Wait for 3 seconds
        pauseStartTime = time.time()
        while time.time() < pauseStartTime+3 :
            self._knob.setHSV(time.time()-pauseStartTime, 1, 1)
        self._knob.setColor(0,0,0)

        # Move the ball back to the center
        self._ballX = self._display.width/2
        self._ballY = self._display.height/2

        # Reset the last update time, since we want to start the game from now
        self._lastUpdateTime = time.time()

    def check_right_goal(self) :
        rightGoal = self._display.width-self._paddleWidth

        if (self._ballX < rightGoal) :
            return False

        posOnPaddle = self._ballY-self._rightPaddlePos

        # Check and see if the ball missed the paddle
        if abs(posOnPaddle) > .6*self._paddleHeight :
            return True

        angle = .5*math.pi*posOnPaddle/self._paddleHeight
        self._ballDx = -math.cos(angle)
        self._ballDy = math.sin(angle)
        return False

    def check_left_goal(self) :
        leftGoal = self._paddleWidth

        if (self._ballX > leftGoal) :
            return False

        posOnPaddle = self._ballY-self._leftPaddlePos

        # Check and see if the ball missed the paddle
        if abs(posOnPaddle) > .6*self._paddleHeight :
            return True

        angle = .5*math.pi*posOnPaddle/self._paddleHeight
        self._ballDx = -math.cos(angle)
        self._ballDy = math.sin(angle)
        return False


    def update_game(self) :
        if self._paused :
            return False

        leftGoal = self._paddleWidth

        if self.check_right_goal() :
            self._leftScore += 1
            self.end_round()
            return

        if self.check_left_goal() :
            self._rightScore += 1
            self.end_round()
            return

        currentTime = time.time()
        dt = currentTime-self._lastUpdateTime
        self._lastUpdateTime = time.time()

        if (self._leftPaddlePos > self._ballY+5) :
            self._leftPaddlePos -= dt*self._leftPaddleSpeed
        if (self._leftPaddlePos < self._ballY-5) :
            self._leftPaddlePos += dt*self._leftPaddleSpeed

        if (self._ballX <= leftGoal) :
            self._ballDx = -self._ballDx

        if (self._ballY >= self._height-1 or
            self._ballY <= 0) :
            self._ballDy = -self._ballDy

        self._ballX += self._ballSpeed*self._ballDx*dt
        self._ballY += self._ballSpeed*self._ballDy*dt

    def draw(self) :
        self._display.clear()

        self._display.drawCircle(self._ballX, self._ballY, 2)

        self._display.drawRect(self._width-self._paddleWidth,
            self._rightPaddlePos-self._paddleHeight/2, self._paddleWidth,
            self._paddleHeight);

        self._display.drawRect(0,
            self._leftPaddlePos-self._paddleHeight/2, self._paddleWidth,
            self._paddleHeight);

        self._display.setCursor(self._width/3, 0)
        self._display.write("%d" % self._leftScore)

        self._display.setCursor(self._width*2/3, 0)
        self._display.write("%d" % self._rightScore)

        if self._paused :
            self._display.setFillColor(.2,.2,.2,0.5)
            self._display.drawRect(25, 10,
                self._width-40, self._height-20)
            self._display.setCursor(0, 15)
            self._display.write("     PAUSED!\n")
            self._display.write("     Press\n")
            self._display.write("     knob to\n")
            self._display.write("     continue\n")

        self._display.refresh()

    def run(self) :
        knobWasPressed = False
        while True :
            self._port.loop()
            knobIsPressed = self._knob.getButton()
            if knobIsPressed and not knobWasPressed :
                self._paused = not self._paused
                self._lastUpdateTime = time.time()
            knobWasPressed = knobIsPressed

            self.update_input()
            self.update_game()
            self.draw()

pong = Pong()
pong.run()

