FROM node:22-alpine AS build

# Set working directory inside the container
WORKDIR /app

# Copy package.json and package-lock.json first to optimize caching
COPY package*.json ./

# Install the dependencies
RUN npm install

# Copy the rest of the application code
COPY . .

# Expose the port Vite's development server will run on (default is 5173)
EXPOSE 5173

# Command to run the Vite development server
CMD ["npm", "run", "dev"]