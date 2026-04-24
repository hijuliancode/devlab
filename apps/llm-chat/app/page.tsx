"use client";

import { useState, useRef, useEffect, FormEvent, KeyboardEvent } from "react";
import { Send, Trash2, Bot, Image as ImageIcon, Volume2, Mic, MicOff, Loader2, Download, MessageSquare } from "lucide-react";
import ReactMarkdown from "react-markdown";

type MessageType = "text" | "image" | "audio";
type Mode = "chat" | "image" | "tts";
type Provider = "openai" | "anthropic";

interface Message {
  role: "user" | "assistant" | "system";
  content: string;
  type?: MessageType;
  imageB64?: string;
  audioUrl?: string;
}

export default function Home() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  const [mode, setMode] = useState<Mode>("chat");
  const [provider, setProvider] = useState<Provider>("openai");
  const [isRecording, setIsRecording] = useState(false);
  const [isSpeaking, setIsSpeaking] = useState(false);
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const chunksRef = useRef<Blob[]>([]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isLoading]);

  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = "auto";
      textareaRef.current.style.height = `${Math.min(textareaRef.current.scrollHeight, 200)}px`;
    }
  }, [input]);

  // DONE: Implementa el envío de mensajes de chat  →  POST /api/chat
  //
  // Flujo:
  //   1. Lee y valida input.trim(). Si está vacío o isLoading, retorna.
  //   2. Agrega el mensaje del usuario a messages[].
  //   3. Limpia el textarea y activa isLoading = true.
  //   4. fetch("POST /api/chat", body: { messages, provider })
  //   5. Si data.error, agrega un mensaje de error del asistente.
  //      Si no, agrega data.message a messages[].
  //   6. En el bloque finally: isLoading = false, enfoca el textarea.
  const sendMessage = async (e?: FormEvent) => {
    if (e) e.preventDefault();

    const trimmedInput = input.trim();

    if (!trimmedInput || isLoading) return;

    const userMessage: Message = {
      role: 'user',
      content: trimmedInput,
    }

    const updatedMessages = [...messages, userMessage];

    setMessages(updatedMessages);
    setInput('');
    setIsLoading(true);


    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
    }

    try {
      const res = await fetch('/api/chat', {
        method: 'POST',
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ messages: updatedMessages, provider }),
      })

      const data = await res.json();

      if (data.error) {
        setMessages([
          ...updatedMessages,
          { role: 'assistant', content: `Error: ${data.error}` }
        ])
      } else {
        setMessages([
          ...updatedMessages,
          data.message
        ])
      }

    } catch (error) {
      setMessages([
        ...updatedMessages,
        {
          role: 'assistant',
          content: `Error: ${error instanceof Error ? error.message : 'Error desconocido'}`
        }
      ])
    } finally {
      setIsLoading(false);
      textareaRef.current?.focus();
    }

  };

  const handleKeyDown = (e: KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  };

  const clearChat = () => {
    setMessages([]);
    setInput('');
    textareaRef.current?.focus();
  };

  // TODO: Implementa la generación de imágenes  →  POST /api/image
  //
  // Flujo:
  //   1. Valida input.trim().
  //   2. Agrega mensaje de usuario con type: "image".
  //   3. fetch("POST /api/image", body: { prompt })
  //   4. Si data.image.b64 existe, agrega mensaje asistente con
  //      type: "image" e imageB64: data.image.b64.
  const generateImage = async () => {};

  // TODO: Implementa texto a audio  →  POST /api/tts
  //
  // Flujo:
  //   1. Valida input.trim().
  //   2. Agrega mensaje de usuario con type: "audio".
  //   3. fetch("POST /api/tts", body: { text })  →  la respuesta es un Blob de audio.
  //   4. Crea una URL temporal: URL.createObjectURL(blob).
  //   5. Agrega mensaje asistente con type: "audio" y audioUrl: url.
  const sendTTS = async () => {};

  
  const handleSubmit = async (e?: FormEvent) => {
    if (e) e.preventDefault();
    if (mode === 'chat') sendMessage(e);
    if (mode === 'image') generateImage();
    if (mode === 'tts') sendTTS();
  };

  // TODO: Implementa leer un mensaje en voz alta  →  POST /api/tts
  //
  // Flujo:
  //   1. Si isSpeaking es true, retorna.
  //   2. fetch("POST /api/tts", body: { text })  →  Blob de audio.
  //   3. Crea un new Audio(url) y llama .play().
  //   4. En audio.onended: isSpeaking = false y revoca la URL con URL.revokeObjectURL.
  const speakText = async (_text: string) => {};

  // DONE: Implementa la grabación de voz  →  POST /api/stt
  //
  // Flujo para iniciar:
  //   1. navigator.mediaDevices.getUserMedia({ audio: true })
  //   2. Crea un MediaRecorder, acumula chunks en ondataavailable.
  //   3. En onstop: construye Blob "audio/webm", detiene los tracks del stream.
  //   4. fetch("POST /api/stt", body: FormData con el blob)
  //   5. Si data.text, pega el texto en el textarea (setInput).
  //
  // Flujo para detener:
  //   - mediaRecorderRef.current?.stop() y setIsRecording(false).
  const toggleRecording = async () => {

    if ( isRecording ) {
      mediaRecorderRef.current?.stop()
      setIsRecording(false)

      return;
    }

    try {
      console.log('mediaDevices ome:',await navigator.mediaDevices.enumerateDevices())
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
      const mediaRecorder = new MediaRecorder(stream)

      mediaRecorderRef.current = mediaRecorder
      chunksRef.current = []

      mediaRecorder.ondataavailable = (e) => {
        if (e.data.size > 0) chunksRef.current.push(e.data)
      }

      mediaRecorder.onstop = async () => {
        const blob = new Blob(chunksRef.current, { type: 'audio/webm' })
        stream.getTracks().forEach((t) => t.stop())

        setIsLoading(true)

        try {
          const formData = new FormData()
          formData.append('audio', blob, 'recording.webm')

          const res = await fetch('/api/stt', { method: 'POST', body: formData })
          const data = await res.json()

          if (data.error) {
            console.error('STT error: ', data.error)  
          } else if (data.text) {
            setInput((prev) => (prev ? `${prev} ${data.text}` : data.text ))
          }

        } catch(err) {
          console.error('STT failed: ', err)
        } finally {
          setIsLoading(false)
          textareaRef.current?.focus();
        }

      }

      mediaRecorder.start();
      setIsRecording(true)

    } catch (err) {
      console.error('Recording failed:', err)
    }
  };

  return (
    <div className="flex h-dvh flex-col bg-background">
      {/* Header */}
      <header className="border-b border-border">
        <div className="flex items-center justify-between px-4 py-3 sm:px-6">
          <div className="flex items-center gap-2.5">
            <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-foreground">
              <Bot className="h-4.5 w-4.5 text-background" />
            </div>
            <h1 className="text-lg font-semibold tracking-tight">altas-GPT</h1>
          </div>
          <div className="flex items-center gap-2">
            <select
              value={provider}
              onChange={(e) => {
                const val = e.target.value as Provider;
                setProvider(val);
                if (val === "anthropic") setMode("chat");
              }}
              className="rounded-lg border border-border bg-muted px-2.5 py-1.5 text-xs font-medium text-foreground focus:border-foreground/20 focus:outline-none"
            >
              <option value="openai">OpenAI</option>
              <option value="anthropic">Anthropic</option>
            </select>
            <button
              onClick={clearChat}
              className="rounded-lg p-2 text-muted-foreground transition-colors hover:bg-muted hover:text-foreground"
              title="Limpiar chat"
            >
              <Trash2 className="h-4.5 w-4.5" />
            </button>
          </div>
        </div>
      </header>

      {/* Messages */}
      <main className="flex-1 overflow-y-auto">
        <div className="mx-auto max-w-2xl px-4 py-6 sm:px-6">
          {messages.length === 0 && !isLoading && (
            <div className="flex h-full min-h-[60vh] flex-col items-center justify-center gap-4 text-center">
              <div className="flex h-14 w-14 items-center justify-center rounded-2xl bg-muted">
                <Bot className="h-7 w-7 text-muted-foreground" />
              </div>
              <div>
                <h2 className="text-xl font-semibold tracking-tight">
                  Hola, soy altas-GPT
                </h2>
                <p className="mt-1.5 text-sm text-muted-foreground">
                  {mode === "chat" && "Escribe un mensaje para comenzar la conversación."}
                  {mode === "image" && "Describe la imagen que quieres generar con DALL-E 3."}
                  {mode === "tts" && "Escribe un texto para convertirlo en audio."}
                </p>
              </div>
            </div>
          )}

          <div className="space-y-6">
            {messages.map((msg, i) => (
              <div
                key={i}
                className={`flex ${msg.role === "user" ? "justify-end" : "justify-start"}`}
              >
                <div
                  className={`max-w-[85%] sm:max-w-[75%] ${
                    msg.role === "user"
                      ? "rounded-2xl rounded-br-md bg-user-bubble px-4 py-2.5 text-user-bubble-text"
                      : "prose-chat text-foreground"
                  }`}
                >
                  {msg.role === "user" ? (
                    <p className="whitespace-pre-wrap text-[0.9375rem] leading-relaxed">
                      {msg.content}
                    </p>
                  ) : msg.type === "image" && msg.imageB64 ? (
                    <div className="space-y-2">
                      <img
                        src={`data:image/png;base64,${msg.imageB64}`}
                        alt={msg.content}
                        className="max-w-full rounded-xl border border-border"
                      />
                      <div className="flex items-center justify-between gap-2">
                        <p className="text-xs text-muted-foreground italic truncate">
                          {msg.content}
                        </p>
                        <button
                          onClick={() => {
                            const link = document.createElement("a");
                            link.href = `data:image/png;base64,${msg.imageB64}`;
                            link.download = `altas-gpt-${Date.now()}.png`;
                            link.click();
                          }}
                          className="inline-flex shrink-0 items-center gap-1.5 rounded-lg px-2 py-1 text-xs text-muted-foreground transition-colors hover:bg-muted hover:text-foreground"
                          title="Descargar imagen PNG"
                        >
                          <Download className="h-3.5 w-3.5" />
                          Descargar
                        </button>
                      </div>
                    </div>
                  ) : msg.type === "audio" && msg.audioUrl ? (
                    <div className="space-y-2">
                      <p className="text-xs text-muted-foreground italic">
                        {msg.content}
                      </p>
                      <audio
                        controls
                        src={msg.audioUrl}
                        className="w-full max-w-xs"
                      />
                      <button
                        onClick={() => {
                          const link = document.createElement("a");
                          link.href = msg.audioUrl!;
                          link.download = `altas-gpt-${Date.now()}.mp3`;
                          link.click();
                        }}
                        className="inline-flex items-center gap-1.5 rounded-lg px-2 py-1 text-xs text-muted-foreground transition-colors hover:bg-muted hover:text-foreground"
                        title="Descargar audio MP3"
                      >
                        <Download className="h-3.5 w-3.5" />
                        Descargar audio
                      </button>
                    </div>
                  ) : (
                    <div className="space-y-1">
                      <div className="text-[0.9375rem] leading-relaxed">
                        <ReactMarkdown>{msg.content}</ReactMarkdown>
                      </div>
                      {provider === "openai" && (
                        <button
                          onClick={() => speakText(msg.content)}
                          disabled={isSpeaking}
                          className="mt-1 inline-flex items-center gap-1.5 rounded-lg px-2 py-1 text-xs text-muted-foreground transition-colors hover:bg-muted hover:text-foreground disabled:opacity-40"
                          title="Escuchar respuesta"
                        >
                          {isSpeaking ? (
                            <Loader2 className="h-3.5 w-3.5 animate-spin" />
                          ) : (
                            <Volume2 className="h-3.5 w-3.5" />
                          )}
                          Escuchar
                        </button>
                      )}
                    </div>
                  )}
                </div>
              </div>
            ))}

            {isLoading && (
              <div className="flex justify-start">
                <div className="flex items-center gap-1.5 px-1 py-2">
                  <span className="typing-dot h-2 w-2 rounded-full bg-muted-foreground" />
                  <span className="typing-dot h-2 w-2 rounded-full bg-muted-foreground" />
                  <span className="typing-dot h-2 w-2 rounded-full bg-muted-foreground" />
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>
        </div>
      </main>

      {/* Input */}
      <footer className="border-t border-border bg-background">
        {/* Mode Tabs */}
        {provider === "openai" && (
          <div className="mx-auto flex max-w-2xl justify-center gap-1 px-4 pt-3 sm:px-6">
            {([
              { key: "chat" as Mode, label: "Texto", icon: MessageSquare },
              { key: "image" as Mode, label: "Imagen", icon: ImageIcon },
              { key: "tts" as Mode, label: "Texto a Audio", icon: Volume2 },
            ]).map(({ key, label, icon: Icon }) => (
              <button
                key={key}
                onClick={() => setMode(key)}
                className={`flex items-center gap-1.5 rounded-lg px-3 py-1.5 text-xs font-medium transition-colors ${
                  mode === key
                    ? "bg-foreground text-background"
                    : "text-muted-foreground hover:bg-muted hover:text-foreground"
                }`}
              >
                <Icon className="h-3.5 w-3.5" />
                {label}
              </button>
            ))}
          </div>
        )}
        <form
          onSubmit={handleSubmit}
          className="mx-auto flex max-w-2xl items-end gap-3 px-4 py-3 sm:px-6"
        >
          {mode === "chat" && provider === "openai" && (
            <button
              type="button"
              onClick={toggleRecording}
              disabled={isLoading}
              className={`flex h-11 w-11 shrink-0 items-center justify-center rounded-xl transition-colors self-end ${
                isRecording
                  ? "bg-red-500 text-white animate-pulse"
                  : "bg-muted text-muted-foreground hover:text-foreground"
              } disabled:opacity-30`}
              title={isRecording ? "Detener grabación" : "Dictar con voz"}
            >
              {isRecording ? (
                <MicOff className="h-4.5 w-4.5" />
              ) : (
                <Mic className="h-4.5 w-4.5" />
              )}
            </button>
          )}
          <textarea
            ref={textareaRef}
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder={
              isRecording
                ? "Grabando... toca el mic para detener"
                : mode === "chat"
                  ? "Escribe un mensaje..."
                  : mode === "image"
                    ? "Describe la imagen a generar..."
                    : "Escribe el texto a convertir en audio..."
            }
            rows={1}
            className="flex-1 resize-none rounded-xl border border-border bg-muted px-4 py-3 text-[0.9375rem] leading-relaxed text-foreground placeholder:text-muted-foreground focus:border-foreground/20 focus:outline-none"
          />
          <button
            type="submit"
            disabled={!input.trim() || isLoading}
            className="flex h-11 w-11 shrink-0 items-center justify-center rounded-xl bg-foreground text-background transition-opacity hover:opacity-80 disabled:opacity-30"
          >
            {isLoading ? (
              <Loader2 className="h-4.5 w-4.5 animate-spin" />
            ) : (
              <Send className="h-4.5 w-4.5" />
            )}
          </button>
        </form>
      </footer>
    </div>
  );
}
