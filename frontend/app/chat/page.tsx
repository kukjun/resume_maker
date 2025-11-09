'use client'

import { useState, useEffect, useRef } from 'react'
import { useRouter } from 'next/navigation'
import { ChatMessage } from '@/components/chat/ChatMessage'
import { ChatInput } from '@/components/chat/ChatInput'

interface Message {
  role: 'user' | 'assistant'
  content: string
}

export default function ChatPage() {
  const router = useRouter()
  const [messages, setMessages] = useState<Message[]>([])
  const [isLoading, setIsLoading] = useState(false)
  const [sessionId, setSessionId] = useState<string | null>(null)
  const [userId, setUserId] = useState<string | null>(null)
  const messagesEndRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    // 세션 ID와 사용자 ID 확인
    const storedSessionId = localStorage.getItem('session_id')
    const storedUserId = localStorage.getItem('user_id')
    if (!storedSessionId || !storedUserId) {
      router.push('/upload')
      return
    }
    setSessionId(storedSessionId)
    setUserId(storedUserId)

    // 첫 질문 가져오기
    const firstQuestion = localStorage.getItem('first_question')
    if (firstQuestion) {
      setMessages([
        {
          role: 'assistant',
          content: firstQuestion,
        },
      ])
      localStorage.removeItem('first_question')
    } else {
      setMessages([
        {
          role: 'assistant',
          content: '안녕하세요! 업로드하신 이력서를 분석했습니다. 더 나은 이력서를 만들기 위해 몇 가지 질문을 드리겠습니다.',
        },
      ])
    }
  }, [router])

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  const handleSendMessage = async (content: string) => {
    if (!sessionId || !userId) return

    // 사용자 메시지 추가
    const userMessage: Message = { role: 'user', content }
    setMessages((prev) => [...prev, userMessage])
    setIsLoading(true)

    try {
      const response = await fetch('http://localhost:8000/api/chat/message', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          session_id: sessionId,
          user_id: userId,
          message: content,
        }),
      })

      if (!response.ok) throw new Error('Failed to send message')

      const data = await response.json()

      // AI 응답 추가
      const assistantMessage: Message = {
        role: 'assistant',
        content: data.response,
      }
      setMessages((prev) => [...prev, assistantMessage])

      // 질문이 완료되면 지식 베이스 페이지로 이동
      if (data.is_completed) {
        setTimeout(() => {
          router.push('/knowledge')
        }, 2000)
      }
    } catch (error) {
      console.error('Send message error:', error)
      alert('메시지 전송 중 오류가 발생했습니다.')
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <main className="flex flex-col h-screen">
      <header className="border-b p-4">
        <h1 className="text-xl font-bold">AI 인터뷰</h1>
      </header>

      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.map((message, index) => (
          <ChatMessage key={index} message={message} />
        ))}
        {isLoading && (
          <div className="flex justify-start">
            <div className="bg-secondary rounded-lg p-4">
              <div className="flex space-x-2">
                <div className="w-2 h-2 bg-primary rounded-full animate-bounce" />
                <div className="w-2 h-2 bg-primary rounded-full animate-bounce delay-100" />
                <div className="w-2 h-2 bg-primary rounded-full animate-bounce delay-200" />
              </div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <div className="border-t p-4">
        <ChatInput onSend={handleSendMessage} disabled={isLoading} />
      </div>
    </main>
  )
}
