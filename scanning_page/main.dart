import 'package:camera/camera.dart';
import 'package:flutter/material.dart';
import 'dart:io';
import 'package:video_player/video_player.dart';
import 'widgets.dart';
import 'scanning_page.dart';

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();

  // Fetch available cameras
  final cameras = await availableCameras();
  final firstCamera = cameras.first;

  runApp(MyApp(camera: firstCamera));
}

class MyApp extends StatelessWidget {
  final CameraDescription camera;

  const MyApp({Key? key, required this.camera}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        primarySwatch: Colors.green,
        visualDensity: VisualDensity.adaptivePlatformDensity,
        fontFamily: 'Roboto',
      ),
      home: MyHomePage(camera: camera),
    );
  }
}

class MyHomePage extends StatefulWidget {
  final CameraDescription camera;

  const MyHomePage({Key? key, required this.camera}) : super(key: key);

  @override
  _MyHomePageState createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage>
    with SingleTickerProviderStateMixin {
  late TabController _tabController;
  late ScrollController _scrollController;
  bool _appBarVisible = true;
  VideoPlayerController? _controller;
  bool _videoInitialized = false;
  late Future<void> _loadingFuture;
  File? _recordedVideo;

  // Default response data with environment impact data
  Map<String, dynamic> response = {
  "message": "File uploaded successfully",
  "data": {
    "product details": {
      "brand name": "Celsius",
      "product name": "Live Fit Peach Vibe Sparkling White Peach Edition",
      "product description": "Celsius Live Fit Peach Vibe Sparkling White Peach Edition is an energy drink that is made with green tea extract, taurine, guarana, and ginseng. It has 10 calories and is free of sugar, fat, and aspartame. The drink is designed to help you accelerate your metabolism, burn fat, and live fit.",
      "Packaging description": "The product is in a silver aluminum can with a green and pink label. The can is labeled Celsius Live Fit Peach Vibe Sparkling White Peach Edition.",
      "calorie count": [
        ["serving size in grams", "Not specified"],
        ["energy in kCal", 10]
      ],
      "ingredients": [
        "Carbonated water",
        "Green tea extract",
        "Citric acid",
        "Natural flavors",
        "Taurine",
        "Sucralose",
        "Panax ginseng",
        "Guarana extract",
        "Caffeine",
        "L-tyrosine",
        "Inositol",
        "Niacinamide",
        "Vitamin B12",
        "Calcium pantothenate",
        "Vitamin B6",
        "Sodium chloride",
        "Sodium citrate",
        "Potassium chloride",
        "Calcium chloride",
        "Magnesium citrate",
        "Sodium bicarbonate",
        "Natural colors"
      ],
      "nutritional content": [
        ["Total Fat", "0"],
        ["Sodium", "140"],
        ["Total Carbohydrate", "2"],
        ["Sugars", "2"],
        ["Protein", "0"],
        ["Vitamin B12", "25"],
        ["Niacin", "8"],
        ["Vitamin B6", "1"],
        ["Calcium Pantothenate", "2"],
        ["Taurine", "1000"],
        ["Ginseng", "100"],
        ["Guarana", "150"]
      ],
      "Allergen Information": [
        "Contains 5% juice",
        "Natural flavors",
        "Color added",
        "Green tea extract"
      ],
      "Cautions and Warnings": [
        "Do not consume if you are sensitive to caffeine or stimulants"
      ],
      "Manufacturing Location": "Made in USA",
      "FSSAI license": "Not applicable (US product)"
    },
    "good-bad-ingridients": {
      "good": [
        "Green tea extract",
        "Taurine",
        "Panax ginseng",
        "Guarana extract",
        "Vitamins (B12, B6, Niacinamide, Calcium pantothenate)"
      ],
      "bad": [
        "Sucralose",
        "Caffeine (in high amounts)",
        "Artificial flavors"
      ]
    },
    "tips": {
      "health": [
        "The drink contains caffeine and stimulants, which may not be suitable for everyone.",
        "While sugar-free, it contains artificial sweeteners which some people prefer to avoid.",
        "The high caffeine content (200mg per serving) can lead to health issues if consumed excessively."
      ],
      "environment": [
        "The aluminum can used for packaging requires energy-intensive mining and manufacturing processes.",
        "The transportation of the product from the manufacturing facility to retailers contributes to carbon emissions.",
        "The extensive use of plastic in the product's packaging, including the shrink wrap, can contribute to plastic pollution."
      ],
      "eco-tips": [
        "Consider homemade infused water with fruit and herbs for a natural and refreshing alternative.",
        "Opt for naturally caffeinated beverages like green tea or black coffee.",
        "Explore energy drinks with fewer artificial ingredients and lower caffeine content.",
        "Consider protein shakes or smoothies for a more nutritious energy boost.",
        "Prioritize a balanced diet and regular physical activity for sustained energy levels."
      ]
    },
    "environment_impact": {
      "carbon_footprint": "Not specified",
      "water_usage": "Not specified",
      "packaging_material": "Aluminum can with plastic shrink wrap",
      "recyclability": "Aluminum can is recyclable"
    }
  }
};

  bool _isLoading = false; 

  @override
  void initState() {
    super.initState();

    _loadingFuture = Future.delayed(Duration(seconds: 0));

    _controller = VideoPlayerController.networkUrl(
        Uri.parse('https://flutter.github.io/assets-for-api-docs/assets/videos/bee.mp4'))
      ..initialize().then((_) {
        setState(() {
          _videoInitialized = true;
        });
        _controller?.play();
        _controller?.setLooping(true);
      });

    _tabController = TabController(length: 3, vsync: this); 
    _scrollController = ScrollController();
    _scrollController.addListener(() {
      if (_scrollController.position.pixels > 56 && _appBarVisible) {
        setState(() {
          _appBarVisible = false;
        });
      } else if (_scrollController.position.pixels <= 56 && !_appBarVisible) {
        setState(() {
          _appBarVisible = true;
        });
      }
    });
  }

  @override
  void dispose() {
    _tabController.dispose();
    _scrollController.dispose();
    _controller?.dispose();
    super.dispose();
  }

  Future<void> _navigateToScanningPage() async {
    final result = await Navigator.push(
      context,
      MaterialPageRoute(
        builder: (context) => ScanningPage(
          camera: widget.camera,
          onVideoUpload: _handleVideoUpload, 
        ),
      ),
    );
    if (result is File) {
      setState(() {
        _recordedVideo = result;
        _videoInitialized = false;
        _controller?.dispose();

        _controller = VideoPlayerController.file(_recordedVideo!)
          ..initialize().then((_) {
            setState(() {
              _videoInitialized = true;
            });
            _controller?.play();
            _controller?.setLooping(true);
          });
      });
    }
  }

  Future<void> _handleVideoUpload(File videoFile) async {
    setState(() {
      _isLoading = true;
    });

    await Future.delayed(const Duration(seconds: 2)); 

    setState(() {
      _isLoading = false; 
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      floatingActionButton: FloatingActionButton(
        onPressed: _navigateToScanningPage,
        child: Icon(Icons.camera_alt),
      ),
      body: _isLoading 
          ? LoadingIndicator(
              loadingText: 'Processing Video...', indicatorColor: Colors.blue)
          : Stack(
              children: [
                Positioned.fill(
                  child: _recordedVideo != null && _videoInitialized
                      ? AspectRatio(
                          aspectRatio: _controller!.value.aspectRatio,
                          child: VideoPlayer(_controller!),
                        )
                      : _videoInitialized
                          ? AspectRatio(
                              aspectRatio: _controller!.value.aspectRatio,
                              child: VideoPlayer(_controller!),
                            )
                          : Container(
                              color: Colors.black,
                              child: Center(
                                  child: CircularProgressIndicator(
                                color: Colors.white,
                              ))),
                ),
                SafeArea(
                  child: NestedScrollView(
                    controller: _scrollController,
                    headerSliverBuilder: (context, innerBoxIsScrolled) {
                      return <Widget>[
                        SliverAppBar(
                          backgroundColor: Colors.transparent,
                          expandedHeight:
                              MediaQuery.of(context).size.height / 3,
                          pinned: true,
                          flexibleSpace: FlexibleSpaceBar(
                            title: _appBarVisible ? null : null,
                            centerTitle: true,
                          ),
                          leading: IconButton(
                            icon: Icon(Icons.arrow_back),
                            onPressed: () {
                              Navigator.pop(context);
                            },
                          ),
                          actions: [
                            _appBarVisible ? SizedBox.shrink() : SizedBox.shrink(),
                          ],
                        ),
                      ];
                    },
                    body: Padding(
                      padding: EdgeInsets.only(top: 200),
                      child: Container(
                        decoration: BoxDecoration(
                          color: Colors.white,
                          borderRadius: BorderRadius.only(
                            topLeft: Radius.circular(30),
                            topRight: Radius.circular(30),
                          ),
                        ),
                        child: _buildTabBarView(),
                      ),
                    ),
                  ),
                ),
              ],
            ),
    );
  }

  Widget _buildTabBarView() {
    return DefaultTabController(
      length: 3, 
      child: Column(
        children: [
          SizedBox(height: 24),
          TabBar(
            isScrollable: true,
            indicatorColor: Color(0xFF607D8B),
            labelColor: Color(0xFF607D8B),
            unselectedLabelColor: Colors.grey,
            labelStyle: TextStyle(fontWeight: FontWeight.bold),
            tabs: [
              Tab(text: 'Product Details'),
              Tab(text: 'Environment Impact'),
              Tab(text: 'Health Impact'),
            ],
          ),
          Expanded(
            child: TabBarView(
              children: [
                // Product Details Tab
                _buildProductDetailsTab(),
                // Environment Impact Tab (updated)
                _buildEnvironmentImpactTab(),
                // Health Impact Tab (updated)
                _buildHealthImpactTab(),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildProductDetailsTab() {
    return SingleChildScrollView(
      child: AboutTab(
        title: response['data'] != null
            ? '${response['data']['product details']['brand name']} ${response['data']['product details']['product name']}'
            : 'Unknown Product',
        types: ['Dairy', 'Ready-to-Eat'],
        description: response['data'] != null
            ? '${response['data']['product details']['product description']}\n\n${response['data']['product details']['Packaging description']}'
            : 'No Description Available',
        quantity: response['data'] != null
            ? '${response['data']['product details']['calorie count'][0][1]}g'
            : 'Unknown Quantity',
        price: response['data'] != null
            ? '${response['data']['product details']['calorie count'][1][1]} kCal'
            : 'Unknown Price',
        facts: 'More information about the product',
        locationText: response['data'] != null
            ? '${response['data']['product details']['Manufacturing Location']}'
            : 'Unknown Location',
        ecoscoreStatName: 'Ecoscore',
        ecoscoreStatValue: 75,
      ),
    );
  }

  // Widget for Environment Impact Tab (Updated)
  Widget _buildEnvironmentImpactTab() {
    return SingleChildScrollView(
      child: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Carbon Footprint
            _buildEnvironmentImpactRow(
              icon: Icons.cloud,
              title: "Carbon Footprint",
              value: response['data']['environment_impact']
                  ['carbon_footprint'],
            ),
            SizedBox(height: 16),
            // Water Usage
            _buildEnvironmentImpactRow(
              icon: Icons.water_drop,
              title: "Water Usage",
              value: response['data']['environment_impact']['water_usage'],
            ),
            SizedBox(height: 16),
            // Packaging Material
            _buildEnvironmentImpactRow(
              icon: Icons.eco,
              title: "Packaging Material",
              value: response['data']['environment_impact']
                  ['packaging_material'],
            ),
            SizedBox(height: 16),
            // Recyclability
            _buildEnvironmentImpactRow(
              icon: Icons.recycling,
              title: "Recyclability",
              value:
                  response['data']['environment_impact']['recyclability'],
            ),
            // Environmental Tips
            SizedBox(height: 24),
            Text(
              "Environmental Tips",
              style: TextStyle(
                fontWeight: FontWeight.bold,
                fontSize: 18,
              ),
            ),
            SizedBox(height: 8),
            _buildTipsList(
                response['data']?['tips']?['environment'] as List<String>? ??
                    []),

            SizedBox(height: 16),
            Text(
              "Eco Tips",
              style: TextStyle(
                fontWeight: FontWeight.bold,
                fontSize: 18,
              ),
            ),
            SizedBox(height: 8),
            _buildTipsList(
                response['data']?['tips']?['eco-tips'] as List<String>? ?? []),
          ],
        ),
      ),
    );
  }

  // Widget for Health Impact Tab (Updated)
  Widget _buildHealthImpactTab() {
    return SingleChildScrollView(
      child: Column(
        children: [
          // Nutrition Stats
          BaseStatsTab(
            nutritionStats: response['data'] != null
                ? [
                    for (var nutrient in response['data']['product details']
                        ['nutritional content'])
                      StatRowData(
                          nutrient[0],
                          double.parse(nutrient[1].replaceAll('%', ''))
                              .toInt())
                  ]
                : [],
            ingredientsDescription: response['data'] != null
                ? response['data']['product details']['ingredients']
                    .join(', ')
                : 'No Ingredients Available',
            typeDefenseChips: [],
            chartData: response['data'] != null
                ? [
                    for (var nutrient in response['data']['product details']
                        ['nutritional content'])
                      ChartData(
                          nutrient[0],
                          double.parse(nutrient[1].replaceAll('%', '')))
                  ]
                : [],
          ),
          // Good/Bad Ingredients
          GoodBadIngredientsTab(
            goodIngredients: response['data'] != null
                ? response['data']['good-bad-ingridients']['good']
                : [],
            badIngredients: response['data'] != null
                ? response['data']['good-bad-ingridients']['bad']
                : [],
          ),

          //Health tips
          SizedBox(height: 24),
          Text(
            "Health Tips",
            style: TextStyle(
              fontWeight: FontWeight.bold,
              fontSize: 18,
            ),
          ),
          SizedBox(height: 8),
          _buildTipsList(
              response['data']?['tips']?['health'] as List<String>? ?? []),
        ],
      ),
    );
  }

  // Helper widget to build rows in Environment Impact
  Widget _buildEnvironmentImpactRow({
    required IconData icon,
    required String title,
    required String value,
  }) {
    return Row(
      children: [
        Icon(
          icon,
          color: Colors.green,
          size: 30,
        ),
        SizedBox(width: 16),
        Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              title,
              style: TextStyle(
                fontWeight: FontWeight.bold,
                fontSize: 16,
              ),
            ),
            SizedBox(height: 4),
            Text(
              value,
              style: TextStyle(fontSize: 14),
            ),
          ],
        ),
      ],
    );
  }

  // Helper widget to build list of tips
  Widget _buildTipsList(List<String> tips) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: tips.map((tip) {
        return Padding(
          padding: const EdgeInsets.only(bottom: 8.0),
          child: Row(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Icon(
                Icons.circle,
                size: 8,
              ),
              SizedBox(width: 8),
              Expanded(
                child: Text(
                  tip,
                  style: TextStyle(fontSize: 14),
                ),
              ),
            ],
          ),
        );
      }).toList(),
    );
  }
}