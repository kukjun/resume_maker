'use client'

import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { KnowledgeEditor } from '@/components/knowledge/KnowledgeEditor'

export default function KnowledgePage() {
  const router = useRouter()
  const [knowledgeBase, setKnowledgeBase] = useState<any>(null)
  const [isLoading, setIsLoading] = useState(true)
  const [sessionId, setSessionId] = useState<string | null>(null)

  useEffect(() => {
    const storedSessionId = localStorage.getItem('session_id')
    if (!storedSessionId) {
      router.push('/upload')
      return
    }
    setSessionId(storedSessionId)
    loadKnowledgeBase(storedSessionId)
  }, [router])

  const loadKnowledgeBase = async (sid: string) => {
    try {
      const response = await fetch(`http://localhost:8000/api/knowledge/${sid}`)
      if (!response.ok) throw new Error('Failed to load knowledge base')
      const data = await response.json()
      setKnowledgeBase(data.data)
    } catch (error) {
      console.error('Load knowledge base error:', error)
    } finally {
      setIsLoading(false)
    }
  }

  const handleUpdate = async (path: string, value: any) => {
    if (!sessionId) return

    try {
      const response = await fetch('http://localhost:8000/api/knowledge/update', {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          session_id: sessionId,
          path,
          value,
        }),
      })

      if (!response.ok) throw new Error('Failed to update')
      alert('업데이트되었습니다.')
    } catch (error) {
      console.error('Update error:', error)
      alert('업데이트 중 오류가 발생했습니다.')
    }
  }

  const handleGenerateResume = () => {
    router.push('/generate')
  }

  if (isLoading) {
    return (
      <main className="flex items-center justify-center h-screen">
        <div className="text-center">로딩 중...</div>
      </main>
    )
  }

  return (
    <main className="container mx-auto px-4 py-8">
      <div className="max-w-4xl mx-auto space-y-6">
        <div className="flex justify-between items-center">
          <h1 className="text-3xl font-bold">내 정보 관리</h1>
          <button
            onClick={handleGenerateResume}
            className="px-6 py-2 bg-primary text-primary-foreground rounded-lg hover:bg-primary/90"
          >
            이력서 생성하기
          </button>
        </div>

        <p className="text-muted-foreground">
          AI가 분석한 정보를 확인하고 수정할 수 있습니다.
        </p>

        <KnowledgeEditor
          data={knowledgeBase}
          onUpdate={handleUpdate}
        />
      </div>
    </main>
  )
}
