#!/bin/bash

# Create missing template directories
mkdir -p templates/admin
mkdir -p templates/auth
mkdir -p templates/content
mkdir -p templates/notification
mkdir -p templates/follow
mkdir -p templates/profil
mkdir -p templates/main
mkdir -p templates/regularUser

# Create base template
cat > templates/base.html << 'EOF'
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Social Media{% endblock %}</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.2/css/all.min.css">
</head>
<body class="bg-gray-50 font-sans">
    {% if messages %}
    <div class="fixed top-4 right-4 z-50 space-y-2 max-w-md">
        {% for message in messages %}
        <div class="p-4 rounded-lg shadow-lg {% if message.tags == 'error' %}bg-red-100 text-red-700{% else %}bg-green-100 text-green-700{% endif %}">
            {{ message }}
        </div>
        {% endfor %}
    </div>
    {% endif %}
    
    {% block content %}{% endblock %}
</body>
</html>
EOF

# Create main home template
cat > templates/main/home.html << 'EOF'
{% extends "base.html" %}
{% load static %}

{% block content %}
<nav class="bg-white shadow-md">
    <div class="max-w-7xl mx-auto px-4 py-3">
        <div class="flex justify-between items-center">
            <a href="{% url 'pages:home_page' %}" class="text-2xl font-bold text-indigo-600">
                SocialMedia
            </a>
            
            <div class="flex items-center space-x-4">
                {% if current_user %}
                <a href="{% url 'profil:my_profile' %}" class="text-gray-700 hover:text-indigo-600">
                    <i class="fas fa-user mr-1"></i> Profile
                </a>
                <a href="{% url 'content:create' %}" class="bg-indigo-600 text-white px-4 py-2 rounded-full hover:bg-indigo-700">
                    <i class="fas fa-plus mr-1"></i> Create Post
                </a>
                <form method="POST" action="{% url 'user:logout' %}" class="inline">
                    {% csrf_token %}
                    <button type="submit" class="text-gray-700 hover:text-red-600">
                        <i class="fas fa-sign-out-alt mr-1"></i> Logout
                    </button>
                </form>
                {% else %}
                <a href="{% url 'user:login' %}" class="text-gray-700 hover:text-indigo-600">Login</a>
                <a href="{% url 'user:signup' %}" class="bg-indigo-600 text-white px-4 py-2 rounded-full hover:bg-indigo-700">Sign Up</a>
                {% endif %}
            </div>
        </div>
    </div>
</nav>

<main class="max-w-7xl mx-auto px-4 py-8">
    {% if current_user %}
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <!-- Left sidebar -->
        <div class="lg:col-span-1">
            <div class="bg-white rounded-xl shadow-md p-6 mb-6">
                <div class="flex items-center space-x-4 mb-4">
                    <img src="{{ current_user.profile.avatar_url|default:'https://api.dicebear.com/7.x/avataaars/svg?seed=default' }}" 
                         alt="{{ current_user.username }}" 
                         class="w-16 h-16 rounded-full">
                    <div>
                        <h2 class="font-bold text-lg">{{ current_user.username }}</h2>
                        <p class="text-gray-600 text-sm">{{ current_user.email }}</p>
                    </div>
                </div>
                
                <div class="grid grid-cols-3 gap-4 text-center mb-4">
                    <div>
                        <p class="font-bold text-lg">{{ post_count|default:0 }}</p>
                        <p class="text-gray-600 text-sm">Posts</p>
                    </div>
                    <div>
                        <p class="font-bold text-lg">{{ followers_count|default:0 }}</p>
                        <p class="text-gray-600 text-sm">Followers</p>
                    </div>
                    <div>
                        <p class="font-bold text-lg">{{ following_count|default:0 }}</p>
                        <p class="text-gray-600 text-sm">Following</p>
                    </div>
                </div>
                
                <a href="{% url 'profil:my_profile' %}" 
                   class="block w-full text-center bg-gray-100 text-gray-800 py-2 rounded-lg hover:bg-gray-200">
                    View Profile
                </a>
            </div>
        </div>
        
        <!-- Main content -->
        <div class="lg:col-span-2">
            <!-- Create post form -->
            <div class="bg-white rounded-xl shadow-md p-6 mb-6">
                <form method="POST" action="{% url 'content:create' %}">
                    {% csrf_token %}
                    <textarea name="text" rows="3" 
                              class="w-full border rounded-lg p-3 mb-3" 
                              placeholder="What's on your mind?"></textarea>
                    <div class="flex justify-between">
                        <button type="submit" 
                                class="bg-indigo-600 text-white px-6 py-2 rounded-lg hover:bg-indigo-700">
                            Post
                        </button>
                    </div>
                </form>
            </div>
            
            <!-- Posts feed -->
            <div class="space-y-6">
                {% for post in posts %}
                <div class="bg-white rounded-xl shadow-md p-6">
                    <!-- Post header -->
                    <div class="flex justify-between items-center mb-4">
                        <div class="flex items-center space-x-3">
                            <img src="{{ post.author.profile.avatar_url|default:'https://api.dicebear.com/7.x/avataaars/svg?seed=default' }}" 
                                 alt="{{ post.author.username }}" 
                                 class="w-10 h-10 rounded-full">
                            <div>
                                <h3 class="font-bold">{{ post.author.username }}</h3>
                                <p class="text-gray-500 text-sm">{{ post.created_at|timesince }} ago</p>
                            </div>
                        </div>
                    </div>
                    
                    <!-- Post content -->
                    <div class="mb-4">
                        <p class="text-gray-800">{{ post.text }}</p>
                        {% if post.media_url %}
                        <div class="mt-4">
                            {% if post.media_type == 'IMAGE' %}
                            <img src="{{ post.media_url }}" alt="Post image" class="w-full rounded-lg">
                            {% elif post.media_type == 'VIDEO' %}
                            <video src="{{ post.media_url }}" controls class="w-full rounded-lg"></video>
                            {% endif %}
                        </div>
                        {% endif %}
                    </div>
                    
                    <!-- Post actions -->
                    <div class="flex items-center justify-between border-t pt-4">
                        <button class="flex items-center space-x-1 text-gray-600 hover:text-red-600 like-btn" 
                                data-post-id="{{ post.id }}">
                            <i class="fas fa-heart"></i>
                            <span class="like-count">{{ post.likes.count }}</span>
                        </button>
                        <a href="{% url 'content:detail' post.id %}" 
                           class="flex items-center space-x-1 text-gray-600 hover:text-blue-600">
                            <i class="fas fa-comment"></i>
                            <span>{{ post.replies.count }}</span>
                        </a>
                    </div>
                </div>
                {% empty %}
                <div class="bg-white rounded-xl shadow-md p-12 text-center">
                    <i class="fas fa-newspaper text-4xl text-gray-300 mb-4"></i>
                    <p class="text-gray-500">No posts yet. Be the first to post!</p>
                </div>
                {% endfor %}
            </div>
        </div>
    </div>
    {% else %}
    <!-- Welcome page for non-logged in users -->
    <div class="text-center py-12">
        <h1 class="text-4xl font-bold text-gray-800 mb-6">Welcome to SocialMedia</h1>
        <p class="text-gray-600 text-lg mb-8 max-w-2xl mx-auto">
            Connect with friends, share your thoughts, and discover new content.
        </p>
        <div class="space-x-4">
            <a href="{% url 'user:login' %}" 
               class="bg-indigo-600 text-white px-8 py-3 rounded-full text-lg hover:bg-indigo-700">
                Login
            </a>
            <a href="{% url 'user:signup' %}" 
               class="bg-white text-indigo-600 border border-indigo-600 px-8 py-3 rounded-full text-lg hover:bg-indigo-50">
                Sign Up
            </a>
        </div>
    </div>
    {% endif %}
</main>

{% if current_user %}
<script>
document.addEventListener('DOMContentLoaded', function() {
    // Like functionality
    document.querySelectorAll('.like-btn').forEach(button => {
        button.addEventListener('click', async function() {
            const postId = this.dataset.postId;
            const likeCount = this.querySelector('.like-count');
            
            try {
                const response = await fetch(`/like/content/${postId}/`, {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': '{{ csrf_token }}',
                        'Content-Type': 'application/json'
                    }
                });
                
                const data = await response.json();
                if (data.status === 'liked' || data.status === 'unliked') {
                    likeCount.textContent = data.likes_count;
                    
                    // Update button appearance
                    const icon = this.querySelector('i');
                    if (data.status === 'liked') {
                        icon.classList.remove('far');
                        icon.classList.add('fas');
                        this.classList.add('text-red-600');
                    } else {
                        icon.classList.remove('fas');
                        icon.classList.add('far');
                        this.classList.remove('text-red-600');
                    }
                }
            } catch (error) {
                console.error('Error:', error);
            }
        });
    });
});
</script>
{% endif %}
{% endblock %}
EOF

echo "Templates created successfully!"