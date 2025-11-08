'use client'

import { useState } from 'react'

interface KnowledgeEditorProps {
  data: any
  onUpdate: (path: string, value: any) => void
}

export function KnowledgeEditor({ data, onUpdate }: KnowledgeEditorProps) {
  const [editingPath, setEditingPath] = useState<string | null>(null)
  const [editValue, setEditValue] = useState<string>('')

  if (!data) {
    return <div>데이터가 없습니다.</div>
  }

  const startEdit = (path: string, currentValue: any) => {
    setEditingPath(path)
    setEditValue(JSON.stringify(currentValue, null, 2))
  }

  const saveEdit = () => {
    if (editingPath) {
      try {
        const parsedValue = JSON.parse(editValue)
        onUpdate(editingPath, parsedValue)
        setEditingPath(null)
      } catch (error) {
        alert('유효한 JSON 형식이 아닙니다.')
      }
    }
  }

  const cancelEdit = () => {
    setEditingPath(null)
    setEditValue('')
  }

  return (
    <div className="space-y-6">
      {/* Personal Info */}
      <section className="border rounded-lg p-6">
        <h2 className="text-xl font-bold mb-4">개인 정보</h2>
        {data.personal_info && (
          <div className="space-y-2">
            {Object.entries(data.personal_info).map(([key, value]) => (
              <div key={key} className="flex justify-between items-center">
                <span className="font-medium">{key}:</span>
                <span>{String(value)}</span>
              </div>
            ))}
          </div>
        )}
      </section>

      {/* Careers */}
      <section className="border rounded-lg p-6">
        <h2 className="text-xl font-bold mb-4">경력</h2>
        {data.careers?.map((career: any, index: number) => (
          <div key={index} className="mb-4 p-4 bg-secondary rounded-lg">
            <h3 className="font-bold">{career.company}</h3>
            <p className="text-sm text-muted-foreground">{career.position}</p>
            <p className="text-sm">{career.duration}</p>
            {career.projects?.length > 0 && (
              <div className="mt-2">
                <p className="font-medium">프로젝트:</p>
                <ul className="list-disc list-inside">
                  {career.projects.map((project: any, pIndex: number) => (
                    <li key={pIndex}>{project.name}</li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        ))}
      </section>

      {/* Skills */}
      <section className="border rounded-lg p-6">
        <h2 className="text-xl font-bold mb-4">기술</h2>
        <div className="flex flex-wrap gap-2">
          {data.skills?.map((skill: string, index: number) => (
            <span
              key={index}
              className="px-3 py-1 bg-primary/10 text-primary rounded-full text-sm"
            >
              {skill}
            </span>
          ))}
        </div>
      </section>

      {/* Education */}
      <section className="border rounded-lg p-6">
        <h2 className="text-xl font-bold mb-4">학력</h2>
        {data.education?.map((edu: any, index: number) => (
          <div key={index} className="mb-2">
            <p className="font-bold">{edu.institution}</p>
            <p className="text-sm">{edu.degree} - {edu.major}</p>
            <p className="text-sm text-muted-foreground">{edu.duration}</p>
          </div>
        ))}
      </section>

      {/* Raw JSON Editor (for advanced users) */}
      <section className="border rounded-lg p-6">
        <h2 className="text-xl font-bold mb-4">전체 데이터 (고급)</h2>
        <button
          onClick={() => startEdit('root', data)}
          className="px-4 py-2 bg-secondary rounded-lg hover:bg-secondary/80"
        >
          JSON 편집
        </button>

        {editingPath === 'root' && (
          <div className="mt-4 space-y-2">
            <textarea
              value={editValue}
              onChange={(e) => setEditValue(e.target.value)}
              className="w-full h-64 p-4 border rounded-lg font-mono text-sm"
            />
            <div className="flex gap-2">
              <button
                onClick={saveEdit}
                className="px-4 py-2 bg-primary text-primary-foreground rounded-lg hover:bg-primary/90"
              >
                저장
              </button>
              <button
                onClick={cancelEdit}
                className="px-4 py-2 border rounded-lg hover:bg-secondary"
              >
                취소
              </button>
            </div>
          </div>
        )}
      </section>
    </div>
  )
}
