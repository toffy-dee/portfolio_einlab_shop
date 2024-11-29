'use client'

import { getUrl } from 'aws-amplify/storage'
import { useEffect, useState } from 'react'
import { Card, CardContent } from '@/components/ui/card'
import Image from 'next/image'

interface GalleryItem {
  id: string
  title: string
  price: string
  image: string
  imageUrl?: string
}

export function Gallery() {
  const [galleryItems, setGalleryItems] = useState<GalleryItem[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    async function fetchGallery() {
      try {
        // Fetch the gallery JSON file
        const { url: jsonUrl } = await getUrl({
          path: 'public/data/gallery.json',
          // options: {
          //   accessLevel: 'public'
          // }
        })
        const response = await fetch(jsonUrl)
        const data = await response.json()
        
        // Get signed URLs for all images
        const itemsWithUrls = await Promise.all(
          data.map(async (item: GalleryItem) => {
            console.log('item: ', item);
            const { url: imageUrl } = await getUrl({
              path: `public/images/${item.image}`,
              // options: {
              //   accessLevel: 'public'
              // }
            })
            return { ...item, imageUrl: imageUrl.toString() }
          })
        )
        console.log('itemsWithUrls: ', itemsWithUrls);
        
        setGalleryItems(itemsWithUrls)
      } catch (error) {
        console.error('Error fetching gallery:', error)
      } finally {
        setLoading(false)
      }
    }

    fetchGallery()
  }, [])

  if (loading) {
    return <div>Loading gallery...</div>
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
      {galleryItems.map((item) => (
        <Card key={item.id} className="overflow-hidden">
          <CardContent className="p-0">
            <Image
              src={item.imageUrl || ''}
              alt={item.title}
              width={400}
              height={400}
              className="w-full h-[300px] object-cover"
            />
            <div className="p-4">
              <h3 className="text-2xl">{item.title}</h3>
              <p className="text-muted-foreground">{item.price}</p>
            </div>
          </CardContent>
        </Card>
      ))}
    </div>
  )
} 