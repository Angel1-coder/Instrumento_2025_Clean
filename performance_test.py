#!/usr/bin/env python
"""
Performance Testing Script for Instrumento
Tests website performance and provides optimization recommendations
"""

import time
import requests
from urllib.parse import urljoin

def test_page_load_time(base_url, pages):
    """Test page load times for different pages"""
    print("🚀 Testing Page Load Performance...")
    print("=" * 50)
    
    results = {}
    
    for page_name, page_url in pages.items():
        full_url = urljoin(base_url, page_url)
        print(f"\nTesting: {page_name}")
        print(f"URL: {full_url}")
        
        try:
            start_time = time.time()
            response = requests.get(full_url, timeout=10)
            load_time = time.time() - start_time
            
            results[page_name] = {
                'load_time': load_time,
                'status_code': response.status_code,
                'content_size': len(response.content)
            }
            
            print(f"✅ Load Time: {load_time:.2f}s")
            print(f"   Status: {response.status_code}")
            print(f"   Size: {len(response.content):,} bytes")
            
        except Exception as e:
            print(f"❌ Error: {e}")
            results[page_name] = {'error': str(e)}
    
    return results

def analyze_performance(results):
    """Analyze performance results and provide recommendations"""
    print("\n📊 Performance Analysis")
    print("=" * 50)
    
    successful_tests = {k: v for k, v in results.items() if 'error' not in v}
    
    if not successful_tests:
        print("❌ No successful tests to analyze")
        return
    
    # Calculate averages
    load_times = [v['load_time'] for v in successful_tests.values()]
    avg_load_time = sum(load_times) / len(load_times)
    max_load_time = max(load_times)
    min_load_time = min(load_times)
    
    print(f"📈 Average Load Time: {avg_load_time:.2f}s")
    print(f"🏃 Fastest: {min_load_time:.2f}s")
    print(f"🐌 Slowest: {max_load_time:.2f}s")
    
    # Performance recommendations
    print("\n💡 Optimization Recommendations:")
    
    if avg_load_time > 3.0:
        print("   ⚠️  Average load time is slow (>3s)")
        print("   💡 Consider: CDN, image optimization, caching")
    
    if max_load_time > 5.0:
        print("   ⚠️  Some pages are very slow (>5s)")
        print("   💡 Check: database queries, external APIs, heavy scripts")
    
    if avg_load_time < 1.0:
        print("   ✅ Excellent performance! Keep it up!")
    
    # Content size analysis
    content_sizes = [v['content_size'] for v in successful_tests.values()]
    avg_content_size = sum(content_sizes) / len(content_sizes)
    
    print(f"\n📦 Content Size Analysis:")
    print(f"   Average: {avg_content_size:,.0f} bytes")
    
    if avg_content_size > 500000:  # 500KB
        print("   ⚠️  Large content size detected")
        print("   💡 Consider: image compression, CSS/JS minification")
    
    return results

def main():
    """Main performance testing function"""
    print("🎵 Instrumento Performance Test Suite")
    print("=" * 50)
    
    # Test configuration
    base_url = "http://127.0.0.1:8000"
    test_pages = {
        "Homepage": "/",
        "Products": "/products/",
        "Rental Instruments": "/products/rental-instruments/",
        "Subscription Plans": "/products/subscription-plans/",
        "Special Offers": "/products/special-offers/"
    }
    
    try:
        # Test page load times
        results = test_page_load_time(base_url, test_pages)
        
        # Analyze results
        analyze_performance(results)
        
        print("\n✅ Performance testing completed!")
        print("\n📋 Next Steps:")
        print("   1. Review slow-loading pages")
        print("   2. Optimize images and assets")
        print("   3. Implement caching strategies")
        print("   4. Monitor performance regularly")
        
    except KeyboardInterrupt:
        print("\n⏹️  Testing interrupted by user")
    except Exception as e:
        print(f"\n❌ Testing failed: {e}")

if __name__ == "__main__":
    main()



