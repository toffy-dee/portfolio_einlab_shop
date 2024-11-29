import Link from "next/link"
import Image from "next/image"

export function SiteHeader() {
  return (
    <header className="w-full border-b bg-white">
      <div className="container flex h-20 items-center justify-between">
        <Link href="/" className="flex items-center">
          <Image
            src="/placeholder.svg"
            alt="Einlab Jewelry Logo"
            width={200}
            height={50}
            className="h-12 w-auto object-contain"
          />
        </Link>
        <div className="flex items-center space-x-4">
          <Link href="#" className="text-xl hover:underline">
            ENG
          </Link>
          <Link href="#" className="text-xl hover:underline">
            KR
          </Link>
        </div>
      </div>
    </header>
  )
}

