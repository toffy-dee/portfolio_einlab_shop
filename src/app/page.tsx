import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Instagram } from 'lucide-react'
import Link from "next/link"
import { Gallery } from "@/components/Gallery"

export default function Page() {
  return (
    <div className="min-h-screen bg-[#faf7f5]">
      {/* Hero Section */}
      <section className="py-24 text-center">
        <h1 className="font-pinyon-script text-5xl md:text-6xl lg:text-7xl tracking-wide">
          Einlab Jewelry
        </h1>
        <p className="mt-4 text-muted-foreground text-lg">
          Handcrafted jewelry for everyday elegance
        </p>
      </section>

      {/* Product Categories */}
      <section className="container mx-auto px-4 py-12">
        <Tabs defaultValue="all" className="w-full">
          <TabsList className="grid w-full grid-cols-2 md:grid-cols-4 lg:grid-cols-7 h-auto">
            <TabsTrigger value="all" className="text-lg">All</TabsTrigger>
            <TabsTrigger value="rings" className="text-lg">Rings</TabsTrigger>
            <TabsTrigger value="necklaces" className="text-lg">Necklaces</TabsTrigger>
            <TabsTrigger value="earrings" className="text-lg">Earrings</TabsTrigger>
            <TabsTrigger value="bracelets" className="text-lg">Bracelets</TabsTrigger>
            <TabsTrigger value="pendants" className="text-lg">Pendants</TabsTrigger>
            <TabsTrigger value="silver" className="text-lg">Silver</TabsTrigger>
          </TabsList>
          <TabsContent value="all" className="mt-6">
            <Gallery />
          </TabsContent>
          {/* Add TabsContent for other categories */}
        </Tabs>
      </section>

      {/* Footer */}
      <footer className="border-t bg-white">
        <div className="container mx-auto px-4 py-12">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            <div>
              <h3 className="text-3xl mb-4">Visit Our Store</h3>
              <p className="text-muted-foreground">
                123 Fashion Street
                <br />
                Gangnam-gu, Seoul
                <br />
                South Korea
              </p>
            </div>
            <div>
              <h3 className="text-3xl mb-4">Connect With Us</h3>
              <Link
                href="https://instagram.com/einlab"
                className="flex items-center gap-2 text-muted-foreground hover:text-foreground transition-colors"
              >
                <Instagram className="h-5 w-5" />
                @einlab
              </Link>
            </div>
          </div>
        </div>
      </footer>
    </div>
  )
}

