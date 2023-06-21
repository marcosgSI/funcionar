<!DOCTYPE html>
<head>
    <!-- Define o conjunto de caracteres para o documento -->
    <meta charset="UTF-8">
    <!-- Define a largura da viewport e a escala inicial -->
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <!-- Define o título da página -->
    <title>Chat Sniffer</title>
    <!-- Importa o CSS do Bootstrap -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css" rel="stylesheet">
    <!-- Importa o CSS do Font Awesome -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.1.0/css/all.min.css">
</head>
<body>
    <!-- Cria um container para o conteúdo da página -->
    <div class="container">
        <!-- Cria uma linha com elementos centralizados vertical e horizontalmente -->
        <div class="row justify-content-center align-items-center vh-100">
            <!-- Define uma coluna de largura média -->
            <div class="col-md-6">
                <!-- Cria um cartão para o chat -->
                <div class="card">
                    <!-- Cria o cabeçalho do cartão -->
                    <div class="card-header bg-primary text-white text-center">
                        <h2>Chat Sniffer</h2>
                    </div>
                    <!-- Cria o corpo do cartão -->
                    <div class="card-body">
                        <!-- Cria a área de mensagens do chat -->
                        <div class="chat-messages mb-3" id="chat-messages" style="height: 300px; overflow-y: auto;">
                        </div>
                        <!-- Cria a área de usuários online -->
                        <div class="online-users mb-3" id="online-users">
                            ChatOnline
                        </div>
                        <!-- Cria o campo de entrada do nome de usuário -->
                        <div class="input-group mb-3">
                            <input type="text" id="username" class="form-control" placeholder="Digite seu nome de usuário...">
                        </div>
                        <!-- Cria o campo de entrada da mensagem -->
                        <div class="input-group mb-3">
                            <input type="text" id="message-input" class="form-control" placeholder="Digite sua mensagem...">
                            <!-- Cria o botão de enviar mensagem -->
                            <button class="btn btn-primary" id="send-button"><i class="fas fa-paper-plane"></i> Enviar</button>
                        </div>
                        <!-- Cria botões de ação -->
                        <div class="d-grid gap-2">
                            <button class="btn btn-secondary" id="clear-button"><i class="fas fa-eraser"></i> Limpar mensagem</button>
                            <button class="btn btn-secondary" id="emoji-button"><i class="far fa-smile"></i> Emoji</button>
                            <button class="btn btn-danger" id="leave-button"><i class="fas fa-sign-out-alt"></i> Sair do chat</button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <!-- Importa o Popper.js -->
    <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.11.6/dist/umd/popper.min.js"></script>
    <!-- Importa o JavaScript do Bootstrap -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/js/bootstrap.min.js"></script>
    <script>
        // Seleciona os elementos HTML
        const chatMessages = document.getElementById("chat-messages");
        const messageInput = document.getElementById("message-input");
        const sendButton = document.getElementById("send-button");
        const usernameInput = document.getElementById("username");
        const clearButton = document.getElementById("clear-button");
        const emojiButton = document.getElementById("emoji-button");
        const leaveButton = document.getElementById("leave-button");
        const onlineUsers = document.getElementById("online-users");
        let serverUrl = "https://servidorchatprincipal.onrender.com/messages"

        // Função para adicionar uma mensagem ao chat
        function addMessage(username, message) {
            const messageElement = document.createElement("div");
            messageElement.textContent = `${username}: ${message}`;
            chatMessages.appendChild(messageElement);
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }

        // Função para buscar mensagens do servidor
        async function fetchMessages() {
            const response = await fetch(serverUrl);
            const messages = await response.json();
            chatMessages.innerHTML = "";
            messages.forEach(({username, message}) => addMessage(username, message));
        }

        // Função para buscar usuários online
        async function fetchOnlineUsers() {
            const response = await fetch(serverUrl,test ?{method:'GET',body:JSON.stringify({username:usernameInput.value})}:{method:'GET'});
            const users = await response.json();
            console.log(username);
            const onlineUsers = document.getElementById("online-users");
            onlineUsers.textContent = `Usuários online: ${users.join(", ")}`;
        }

        // Função para enviar uma mensagem
        async function sendMessage() {
            test=true
            const message = messageInput.value.trim();
            const username = usernameInput.value.trim();
            if (!message || !username) return;

         // Desabilitar o campo de input do nome do usuário
            usernameInput.disabled = true;
            usernameInput.style.backgroundColor = "#e9ecef";

            messageInput.value = "";
            messageInput.focus();

            const response = await fetch(serverUrl, {
            method: "POST",
            headers: {
            "Content-Type": "application/json"
        },
            body: JSON.stringify({username: username, message: message})
    });

    if (!response.ok) {
                serverUrl = "https://servidorreplicado.onrender.com/messages"
                const response = await fetch(serverUrl, {
                method: "POST",
                headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({username: username, message: message})
    });
            }
}

        // Função para limpar a mensagem
        function clearMessage() {
            messageInput.value = "";
        }

        // Função para inserir um emoji
        function insertEmoji() {
            const emoji = "😀"; 
            messageInput.value += emoji;
            messageInput.focus();
        }

        // Função para sair do chat
        function leaveChat() {
        chatMessages.innerHTML = ""; // Limpar o histórico de mensagens do chat
        window.location.reload();
}


        // Adiciona eventos aos elementos HTML
        sendButton.addEventListener("click", sendMessage);
        messageInput.addEventListener("keydown", (event) => {
            if (event.key === "Enter") {
                sendMessage();
            }
        });
        clearButton.addEventListener("click", clearMessage);
        emojiButton.addEventListener("click", insertEmoji);
        leaveButton.addEventListener("click", leaveChat);

        // Busca mensagens e usuários online
        fetchMessages();
        fetchOnlineUsers();
        setInterval(fetchMessages, 3000);
        setInterval(fetchOnlineUsers, 5000);
    </script>
</body>
</html>
