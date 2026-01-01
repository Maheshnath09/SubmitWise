FROM node:18-alpine

WORKDIR /app

# Copy package files
COPY package.json ./

# Install dependencies
RUN npm install

# Copy all files
COPY . .

# Expose port
EXPOSE 3000

# Set environment variable
ENV NEXT_PUBLIC_API_URL=http://localhost:8000

# Run in development mode (simpler, no build issues)
CMD ["npm", "run", "dev"]

