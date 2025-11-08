import Link from 'next/link'

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-24">
      <div className="text-center space-y-8">
        <h1 className="text-4xl font-bold">Resume Maker</h1>
        <p className="text-xl text-muted-foreground">
          AI가 당신의 이력서를 JD에 맞춰 최적화합니다
        </p>

        <div className="flex gap-4 justify-center">
          <Link
            href="/upload"
            className="px-6 py-3 bg-primary text-primary-foreground rounded-lg hover:bg-primary/90 transition"
          >
            시작하기
          </Link>
          <Link
            href="/knowledge"
            className="px-6 py-3 border border-border rounded-lg hover:bg-secondary transition"
          >
            내 정보 관리
          </Link>
        </div>
      </div>
    </main>
  )
}
