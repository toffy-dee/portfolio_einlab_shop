/** @type {import('next').NextConfig} */
const nextConfig = {
  images: {
    remotePatterns: [{
      protocol: 'https',
      hostname: 'einlab-storage-gallery4ca51-dev.s3.eu-central-1.amazonaws.com'
    }]
  }
}

module.exports = nextConfig 