FROM node:19-alpine

WORKDIR /app

# Copy package files and install dependencies
COPY package.json package-lock.json ./
RUN npm install

# Copy all files
COPY . .

# Set environment variables
ENV NODE_ENV=production
ENV REACT_APP_API_URL=https://1jjdwnh7k5.execute-api.us-east-1.amazonaws.com/Prod

EXPOSE 3000

# Start the app
CMD ["npm", "start"]