async function askQuestion() {
  const input = document.getElementById("question");

  const chatBox = document.getElementById("chat-box");

  const question = input.value.trim();

  if (!question) return;

  chatBox.innerHTML += `
        <div class="user">
            ${question}
        </div>
    `;

  input.value = "";

  const loadingId = "loading-" + Date.now();

  chatBox.innerHTML += `
        <div
            class="bot"
            id="${loadingId}"
        >
            Thinking...
        </div>
    `;

  chatBox.scrollTop = chatBox.scrollHeight;

  try {
    const response = await fetch("/ask", {
      method: "POST",

      headers: {
        "Content-Type": "application/json",
      },

      body: JSON.stringify({
        question: question,
      }),
    });

    const data = await response.json();

    document.getElementById(loadingId).remove();

    chatBox.innerHTML += `
            <div class="bot">
                ${marked.parse(data.answer)}
            </div>
        `;

    chatBox.scrollTop = chatBox.scrollHeight;
  } catch (error) {
    const loadingElement = document.getElementById(loadingId);

    if (loadingElement) {
      loadingElement.remove();
    }

    chatBox.innerHTML += `
            <div class="bot">
                Error occurred while
                generating response.
            </div>
        `;

    console.error(error);
  }
}

document
  .getElementById("question")
  .addEventListener("keypress", function (event) {
    if (event.key === "Enter") {
      askQuestion();
    }
  });
