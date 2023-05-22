document.addEventListener('DOMContentLoaded', function() {
                                            const form = document.getElementById('message-form');
                                            const chatDisplay = document.getElementById('chat-display');
                                            const userInput = document.getElementById('user-input');
                                          
                                            form.addEventListener('submit', function(event) {
                                              event.preventDefault();
                                              const message = userInput.value;
                                              displayMessage('user', message);
                                              sendMessageToRasa(message);
                                              userInput.value = '';
                                            });
                                          
                                            function displayMessage(sender, message) {
                                              const messageContainer = document.createElement('div');
                                              messageContainer.classList.add('message');
                                              messageContainer.classList.add(sender);
                                              messageContainer.textContent = message;
                                              chatDisplay.appendChild(messageContainer);
                                              chatDisplay.scrollTop = chatDisplay.scrollHeight;
                                            }
                                          
                                            async function sendMessageToRasa(message) {
                                              try {
                                                const response = await fetch('http://localhost:5055/webhook', {
                                                  method: 'POST',
                                                  headers: {
                                                    'Content-Type': 'application/json',
                                                  },
                                                  body: JSON.stringify({
                                                    sender: 'user',
                                                    message: message,
                                                  }),
                                                });
                                                const data = await response.json();
                                                const botResponse = data[0].text;
                                                displayMessage('bot', botResponse);
                                              } catch (error) {
                                                console.error('Error:', error);
                                              }
                                            }
                                          });
                                          