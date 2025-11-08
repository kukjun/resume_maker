'use client'

import { useState } from 'react'

interface JDInputProps {
  onGenerate: (jdText: string, jdUrl: string) => void
  isGenerating: boolean
}

export function JDInput({ onGenerate, isGenerating }: JDInputProps) {
  const [jdText, setJdText] = useState('')
  const [jdUrl, setJdUrl] = useState('')
  const [inputMode, setInputMode] = useState<'text' | 'url'>('text')

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (inputMode === 'text' && jdText.trim()) {
      onGenerate(jdText.trim(), '')
    } else if (inputMode === 'url' && jdUrl.trim()) {
      onGenerate('', jdUrl.trim())
    }
  }

  return (
    <div className="space-y-4">
      <div className="flex gap-2 border-b">
        <button
          type="button"
          onClick={() => setInputMode('text')}
          className={`px-4 py-2 font-medium ${
            inputMode === 'text'
              ? 'border-b-2 border-primary text-primary'
              : 'text-muted-foreground'
          }`}
        >
          JD 텍스트 입력
        </button>
        <button
          type="button"
          onClick={() => setInputMode('url')}
          className={`px-4 py-2 font-medium ${
            inputMode === 'url'
              ? 'border-b-2 border-primary text-primary'
              : 'text-muted-foreground'
          }`}
        >
          JD URL 입력
        </button>
      </div>

      <form onSubmit={handleSubmit} className="space-y-4">
        {inputMode === 'text' ? (
          <textarea
            value={jdText}
            onChange={(e) => setJdText(e.target.value)}
            placeholder="Job Description을 입력하세요..."
            className="w-full h-64 p-4 border rounded-lg focus:outline-none focus:ring-2 focus:ring-primary"
            disabled={isGenerating}
          />
        ) : (
          <input
            type="url"
            value={jdUrl}
            onChange={(e) => setJdUrl(e.target.value)}
            placeholder="https://..."
            className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-primary"
            disabled={isGenerating}
          />
        )}

        <button
          type="submit"
          disabled={
            isGenerating ||
            (inputMode === 'text' ? !jdText.trim() : !jdUrl.trim())
          }
          className="w-full px-6 py-3 bg-primary text-primary-foreground rounded-lg hover:bg-primary/90 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {isGenerating ? '생성 중...' : '이력서 생성'}
        </button>
      </form>
    </div>
  )
}
