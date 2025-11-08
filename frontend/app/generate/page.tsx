'use client'

import { useState } from 'react'
import { JDInput } from '@/components/generate/JDInput'

export default function GeneratePage() {
  const [isGenerating, setIsGenerating] = useState(false)
  const [jobId, setJobId] = useState<string | null>(null)

  const handleGenerate = async (jdText: string, jdUrl: string) => {
    setIsGenerating(true)
    const sessionId = localStorage.getItem('session_id')

    if (!sessionId) {
      alert('세션이 만료되었습니다. 다시 이력서를 업로드해주세요.')
      setIsGenerating(false)
      return
    }

    try {
      const response = await fetch('http://localhost:8000/api/generate/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          session_id: sessionId,
          jd_text: jdText || jdUrl,  // 간단하게 둘 중 하나만 사용
        }),
      })

      if (!response.ok) {
        const error = await response.json()
        throw new Error(error.detail || 'Failed to generate')
      }

      const data = await response.json()
      setJobId(data.job_id)
      setIsGenerating(false)

      // 바로 다운로드
      window.location.href = `http://localhost:8000/api/generate/download/${data.job_id}`
    } catch (error: any) {
      console.error('Generate error:', error)
      alert(error.message || '이력서 생성 중 오류가 발생했습니다.')
      setIsGenerating(false)
    }
  }

  return (
    <main className="container mx-auto px-4 py-16">
      <div className="max-w-2xl mx-auto space-y-8">
        <div className="text-center">
          <h1 className="text-3xl font-bold mb-4">이력서 생성</h1>
          <p className="text-muted-foreground">
            지원하려는 JD를 입력하면 맞춤형 이력서를 생성합니다.
          </p>
        </div>

        <JDInput onGenerate={handleGenerate} isGenerating={isGenerating} />

        {isGenerating && (
          <div className="text-center space-y-4">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto" />
            <p className="text-muted-foreground">이력서를 생성하고 있습니다...</p>
          </div>
        )}
      </div>
    </main>
  )
}
