# QR Code Scanner Feature - NixKart

## Overview
The QR Code Scanner feature allows users to quickly add products to their cart by scanning product QR codes using their device camera or by uploading QR code images.

## Features

### 1. **Camera Scanning**
- Real-time QR code detection using device camera
- Visual scanning frame with corner guides
- Animated scan line for better UX
- Automatic product detection and cart addition
- Support for both front and rear cameras

### 2. **Image Upload**
- Drag and drop QR code images
- File browser selection
- Automatic QR code detection from uploaded images
- Support for common image formats (PNG, JPG, JPEG, WebP)

### 3. **User-Friendly Interface**
- Modern, responsive design
- Tab-based interface (Camera vs Upload)
- Clear instructions and guidance
- Real-time feedback and status messages
- Success/error notifications

## How to Access

### Navigation Bar
- Click the QR code icon (📱) in the top navigation bar

### Cart Page
- Click "Scan QR Code to Add Products" button at the top of the cart
- Click "Scan QR Code" button in the empty cart state

### Direct URL
- Navigate to: `/qr-scanner/`

## How to Use

### Method 1: Camera Scanning

1. **Navigate to QR Scanner**
   - Click the QR icon in the navigation or use the cart button

2. **Start Camera**
   - Click the "Start Camera" button
   - Allow camera permissions when prompted

3. **Scan QR Code**
   - Position the product QR code within the highlighted frame
   - The system will automatically detect and process the code
   - Product will be added to cart instantly

4. **Confirmation**
   - Success message will appear
   - Option to view cart or scan another product

### Method 2: Upload Image

1. **Switch to Upload Tab**
   - Click the "Upload Image" tab

2. **Upload QR Code**
   - Drag and drop an image containing the QR code, OR
   - Click "Choose File" to browse and select an image

3. **Processing**
   - The system automatically detects the QR code
   - Product is added to cart if valid

4. **Confirmation**
   - Success message displays product information
   - Options to view cart or scan another code

## Product QR Codes

### Where to Find QR Codes
- Each product detail page displays a unique QR code
- QR codes are located in the "Quick Add via QR Code" section
- QR codes can be downloaded or printed for physical display

### QR Code Generation
- QR codes are automatically generated for each product
- Codes contain unique URLs pointing to: `/qr-add-to-cart/{product-slug}/`
- Works in both development and production environments

### Scanning Product QR Codes
1. Find the QR code on the product detail page
2. Use the QR Scanner feature to scan it
3. Product is automatically added to your cart

## Technical Implementation

### Frontend Technologies
- **html5-qrcode** (v2.3.8): Camera-based QR code scanning
- **jsQR** (v1.4.0): Image-based QR code detection
- **Modern CSS**: Responsive design with animations
- **Bootstrap 5**: UI components and styling

### Backend Integration
- Django view: `qr_scanner()`
- URL route: `/qr-scanner/`
- QR code processing: `qr_add_to_cart(product_slug)`
- Session-based cart management

### QR Code Format
```
URL Pattern: https://your-domain.com/qr-add-to-cart/{product-slug}/
Example: https://nixkart.com/qr-add-to-cart/wireless-headphones/
```

## Browser Compatibility

### Camera Scanning
- ✅ Chrome/Edge (Desktop & Mobile)
- ✅ Safari (iOS 11+, macOS)
- ✅ Firefox (Desktop & Mobile)
- ✅ Samsung Internet
- ⚠️ Requires HTTPS in production

### Image Upload
- ✅ All modern browsers
- ✅ Works without camera permissions
- ✅ No HTTPS requirement

## Mobile Support

### iOS
- Camera scanning: Supported (iOS 11+)
- Image upload: Supported
- Optimized touch interface

### Android
- Camera scanning: Fully supported
- Image upload: Supported
- Material Design optimizations

## Security & Privacy

### Camera Access
- Camera access is only requested when user clicks "Start Camera"
- Camera feed is processed locally in the browser
- No video/images are uploaded to the server
- Camera can be stopped at any time

### Data Privacy
- QR codes only contain product URLs
- No personal information in QR codes
- Cart operations use existing session management

## Troubleshooting

### Camera Not Working

**Issue**: Camera doesn't start
- **Solution**: Check browser permissions (Settings → Site Settings → Camera)
- **Solution**: Ensure HTTPS is enabled in production
- **Solution**: Try refreshing the page

**Issue**: Camera access denied
- **Solution**: Grant camera permissions in browser settings
- **Solution**: Try using image upload instead

### QR Code Not Detected

**Issue**: QR code not scanning
- **Solution**: Ensure adequate lighting
- **Solution**: Hold camera steady
- **Solution**: Position QR code within the frame
- **Solution**: Try image upload method

**Issue**: Invalid QR code error
- **Solution**: Ensure QR code is from NixKart product page
- **Solution**: Try regenerating the QR code on product detail page

### Product Not Added

**Issue**: Product shows as out of stock
- **Solution**: Check product availability on product detail page
- **Solution**: Contact support if stock appears incorrect

**Issue**: Network error
- **Solution**: Check internet connection
- **Solution**: Refresh page and try again

## Use Cases

### Retail Store
- Print QR codes on product displays
- Customers scan to add items to cart
- Reduces checkout time
- Enables contactless shopping

### Catalog Shopping
- Include QR codes in printed catalogs
- Customers scan directly from catalog
- Quick order placement
- Bridge physical and digital shopping

### Promotional Materials
- Add QR codes to flyers, posters, ads
- Direct product addition from marketing materials
- Track campaign effectiveness

### Warehouse/Inventory
- Quick product lookup and ordering
- Inventory management integration
- Bulk order processing

## Future Enhancements

### Planned Features
- [ ] Bulk scanning (multiple products)
- [ ] Quantity selection during scan
- [ ] Scan history
- [ ] Favorite QR codes
- [ ] Share QR codes via social media
- [ ] NFC support
- [ ] Barcode scanning support
- [ ] AR product preview

### Integration Opportunities
- [ ] Loyalty program integration
- [ ] Wishlist addition via QR
- [ ] Product comparison via QR
- [ ] Review submission via QR

## Support

For issues or questions:
- Email: support@nixkart.com
- Help Center: Available in Support section
- Documentation: This guide

## Version History

### v1.0.0 (Current)
- Initial QR scanner implementation
- Camera and upload support
- Mobile responsive design
- Real-time scanning
- Session-based cart integration

---

**Last Updated**: November 11, 2025
**Maintained by**: NixKart Development Team
