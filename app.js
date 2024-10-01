let score = 0;
let correctAnswer;
let timeLeft;
let timerInterval;
let roundFinished = false;  // To track if the round is over

document.getElementById("answer").addEventListener("keydown", function(event) {
    if (event.key === "Enter") {
        if (!roundFinished) {
            checkAnswer();  // Submit the answer if round is not finished
        } else {
            startGame();  // Start a new round if the previous round has finished
        }
    }
});

function startGame() {
    document.getElementById("feedback").textContent = '';
    document.getElementById("answer").value = '';
    document.getElementById("answer").focus();  // Auto-focus the input field for better UX
    generateNumbers();
    timeLeft = 15;  // Time limit per round
    document.getElementById("timer").textContent = `Time: ${timeLeft}s`;
    timerInterval = setInterval(updateTimer, 1000);
    roundFinished = false;  // Reset round status
}

function generateNumbers() {
    let num1 = Math.floor(Math.random() * 90) + 10;
    let num2 = Math.floor(Math.random() * 90) + 10;
    correctAnswer = num1 + num2;
    document.getElementById("numbers").textContent = `${num1} + ${num2}`;
}

function updateTimer() {
    timeLeft--;
    document.getElementById("timer").textContent = `Time: ${timeLeft}s`;
    if (timeLeft <= 0) {
        clearInterval(timerInterval);
        document.getElementById("feedback").textContent = `⏰ Time's up! The correct answer was ${correctAnswer}.`;
        roundFinished = true;
    }
}

function checkAnswer() {
    clearInterval(timerInterval);  // Stop the timer
    let userAnswer = parseInt(document.getElementById("answer").value);
    if (userAnswer === correctAnswer) {
        document.getElementById("feedback").textContent = "✅ Correct!";
        score++;
    } else {
        document.getElementById("feedback").textContent = `❌ Wrong! The correct answer was ${correctAnswer}.`;
    }
    document.getElementById("score").textContent = score;
    roundFinished = true;  // Mark the round as finished
}

// Start the game when the page loads
startGame();

// run like this:

// 1) python3 -m http.server 8000
// 2) then go to http://localhost:8000/
