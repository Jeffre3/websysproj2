from django.db.models import Count
from .models import Product, Purchase
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from decimal import Decimal

class ProductRecommender:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(stop_words='english')
        
    def get_user_recommendations(self, user, limit=5):
        """Get personalized recommendations for a user based on their purchase history"""
        # Get user's purchase history
        user_purchases = Purchase.objects.filter(user=user)
        if not user_purchases.exists():
            return self.get_popular_products(limit)
            
        # Get products similar to what the user has purchased
        purchased_products = [p.product for p in user_purchases]
        similar_products = []
        
        for purchased_product in purchased_products:
            # Find products in similar price range (±20%)
            price_range = purchased_product.price * Decimal('0.2')
            similar_price_products = Product.objects.filter(
                price__range=(purchased_product.price - price_range, 
                            purchased_product.price + price_range),
                condition=purchased_product.condition,
                is_sold=False
            ).exclude(id__in=[p.id for p in purchased_products])
            
            similar_products.extend(similar_price_products)
        
        # If we don't have enough similar products, add popular products
        if len(similar_products) < limit:
            popular_products = self.get_popular_products(limit - len(similar_products))
            similar_products.extend(popular_products)
            
        return similar_products[:limit]
    
    def get_popular_products(self, limit=5):
        """Get most popular products based on purchase history"""
        return Product.objects.filter(is_sold=False).annotate(
            purchase_count=Count('purchase')
        ).order_by('-purchase_count')[:limit]
    
    def get_similar_products(self, product, limit=5):
        """Get products similar to a given product based on description and price"""
        # Get all active products except the current one
        other_products = Product.objects.filter(is_sold=False).exclude(id=product.id)
        
        if not other_products.exists():
            return []
            
        # Create TF-IDF matrix for product descriptions
        descriptions = [product.description] + [p.description for p in other_products]
        tfidf_matrix = self.vectorizer.fit_transform(descriptions)
        
        # Calculate similarity scores
        similarity_scores = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:])
        
        # Get indices of most similar products
        similar_indices = similarity_scores[0].argsort()[-limit:][::-1]
        
        return [other_products[i] for i in similar_indices] 