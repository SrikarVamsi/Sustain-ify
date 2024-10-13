import 'package:flutter/material.dart';
import 'package:syncfusion_flutter_charts/charts.dart';

// Loading Indicator Widget
class LoadingIndicator extends StatelessWidget {
  final String loadingText;
  final Color indicatorColor;

  LoadingIndicator(
      {this.loadingText = 'Loading...', this.indicatorColor = Colors.green});

  @override
  Widget build(BuildContext context) {
    return Center(
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          CircularProgressIndicator(
            valueColor: AlwaysStoppedAnimation<Color>(indicatorColor),
            strokeWidth: 5,
          ),
          SizedBox(height: 20),
          Text(
            loadingText,
            style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
          ),
        ],
      ),
    );
  }
}

// Type Chip Widget
class TypeChip extends StatelessWidget {
  final String type;
  final Color? backgroundColor;

  TypeChip({required this.type, this.backgroundColor});

  @override
  Widget build(BuildContext context) {
    Color chipBackgroundColor = backgroundColor ?? Colors.grey; // Default color
    switch (type) {
      case 'Dairy':
        chipBackgroundColor = Colors.blue[300]!;
        break;
      case 'Ready-to-Eat':
        chipBackgroundColor = Colors.green[300]!;
        break;
      // Add more cases as needed
    }

    return Container(
      padding: EdgeInsets.symmetric(horizontal: 16, vertical: 8),
      decoration: BoxDecoration(
        color: chipBackgroundColor,
        borderRadius: BorderRadius.circular(20),
      ),
      child: Text(
        type,
        style: TextStyle(
          color: Colors.white,
          fontWeight: FontWeight.bold,
        ),
      ),
    );
  }
}

// About Tab Widget
class AboutTab extends StatelessWidget {
  final String title;
  final List<String> types;
  final String description;
  final String quantity;
  final String price;
  final String facts;
  final String locationText;
  final String ecoscoreStatName;
  final int ecoscoreStatValue;

  AboutTab({
    required this.title,
    required this.types,
    required this.description,
    required this.quantity,
    required this.price,
    required this.facts,
    required this.locationText,
    required this.ecoscoreStatName,
    required this.ecoscoreStatValue,
  });

  @override
  Widget build(BuildContext context) {
    return SingleChildScrollView(
      padding: EdgeInsets.all(20.0),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Center(
            child: Column(
              children: [
                Text(
                  title,
                  style: TextStyle(
                    fontSize: 36,
                    fontWeight: FontWeight.bold,
                  ),
                ),
                SizedBox(height: 8),
                Row(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children:
                      types.map((type) => TypeChip(type: type)).toList(),
                ),
              ],
            ),
          ),
          SizedBox(height: 20),
          Text(
            description,
            style: TextStyle(fontSize: 16),
          ),
          SizedBox(height: 20),
          Container(
            padding: EdgeInsets.all(16.0),
            decoration: BoxDecoration(
              color: Colors.white,
              borderRadius: BorderRadius.circular(10.0),
            ),
            child: Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Text('Quantity',
                    style:
                        TextStyle(fontWeight: FontWeight.bold, fontSize: 18)),
                Text(quantity),
              ],
            ),
          ),
          SizedBox(height: 10),
          Container(
            padding: EdgeInsets.all(16.0),
            decoration: BoxDecoration(
              color: Colors.white,
              borderRadius: BorderRadius.circular(10.0),
            ),
            child: Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Text('Price',
                    style:
                        TextStyle(fontWeight: FontWeight.bold, fontSize: 18)),
                Text(price),
              ],
            ),
          ),
          SizedBox(height: 20),
          Text(
            'Facts',
            style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
          ),
          SizedBox(height: 10),
          Text(
            facts,
            style: TextStyle(fontSize: 16),
          ),
          SizedBox(height: 20),
          Text(
            'Location',
            style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
          ),
          SizedBox(height: 10),
          Container(
            height: 200,
            color: Colors.grey[300],
            child: Center(child: Text(locationText)),
          ),
          SizedBox(height: 20),
          Text(
            'Ecoscore',
            style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
          ),
          SizedBox(height: 10),
          StatRow(statName: ecoscoreStatName, statValue: ecoscoreStatValue),
        ],
      ),
    );
  }
}


// Base Stats Tab Widget
class BaseStatsTab extends StatelessWidget {
  final List<StatRowData> nutritionStats;
  final String ingredientsDescription;
  final List<TypeDefenseChipData> typeDefenseChips;
  final List<ChartData> chartData;

  BaseStatsTab({
    required this.nutritionStats,
    required this.ingredientsDescription,
    required this.typeDefenseChips,
    required this.chartData,
  });

  @override
  Widget build(BuildContext context) {
    return SingleChildScrollView(
      padding: const EdgeInsets.symmetric(horizontal: 24.0),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            'Nutrition',
            style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
          ),
          SizedBox(height: 10),
          ...nutritionStats
              .map((stat) => StatRow(statName: stat.name, statValue: stat.value))
              .toList(),
          SizedBox(height: 20),
          Text(
            'Ingredients',
            style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
          ),
          SizedBox(height: 10),
          Text(
            ingredientsDescription,
            style: TextStyle(fontSize: 16),
          ),
          SizedBox(height: 20),
          Text(
            'Nutritional Breakdown',
            style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
          ),
          SizedBox(height: 10),
          Container(
            height: 400, // Increased height to accommodate the legends
            child: SfCircularChart(
              title: ChartTitle(text: 'Nutrition Chart'),
              legend: Legend(
                isVisible: true,
                overflowMode: LegendItemOverflowMode.wrap,
                position: LegendPosition.bottom,
              ),
              series: <PieSeries<ChartData, String>>[
                PieSeries<ChartData, String>(
                  dataSource: chartData,
                  xValueMapper: (ChartData data, _) => data.category,
                  yValueMapper: (ChartData data, _) => data.value,
                  dataLabelSettings: DataLabelSettings(isVisible: true),
                  name: 'Nutrition',
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}


// Good/Bad Ingredients Tab Widget
// Good/Bad Ingredients Tab Widget (Improved Styling and Overflow Handling)
class GoodBadIngredientsTab extends StatelessWidget {
  final List<String> goodIngredients;
  final List<String> badIngredients;

  GoodBadIngredientsTab(
      {required this.goodIngredients, required this.badIngredients});

  @override
  Widget build(BuildContext context) {
    return SingleChildScrollView(
      padding: EdgeInsets.all(20),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          _buildIngredientSection(
              'Good Ingredients', goodIngredients, Colors.green),
          SizedBox(height: 20),
          _buildIngredientSection('Ingredients to Consider', badIngredients,
              Colors.orange),
        ],
      ),
    );
  }

  // Helper function to build the ingredient section with tiles
  Widget _buildIngredientSection(
      String title, List<String> ingredients, Color color) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          title,
          style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
        ),
        SizedBox(height: 10),
        Wrap(
          spacing: 8.0, // Spacing between tiles
          runSpacing: 4.0, // Spacing between rows
          children: ingredients.map((ingredient) {
            return _buildIngredientTile(ingredient, color);
          }).toList(),
        ),
      ],
    );
  }

  // Helper function to build a single ingredient tile
  Widget _buildIngredientTile(String ingredient, Color color) {
    return Container(
      padding: EdgeInsets.symmetric(horizontal: 12, vertical: 6),
      decoration: BoxDecoration(
        color: color.withOpacity(0.2),
        borderRadius: BorderRadius.circular(20),
        border: Border.all(color: color),
      ),
      child: Text(
        ingredient,
        style: TextStyle(
          color: color,
          fontWeight: FontWeight.bold,
        ),
      ),
    );
  }
}
// Tips Tab Widget
class TipsTab extends StatelessWidget {
  final List<String> healthTips;
  final List<String> environmentTips;
  final List<String> ecoTips;

  TipsTab(
      {required this.healthTips,
      required this.environmentTips,
      required this.ecoTips});

  @override
  Widget build(BuildContext context) {
    return SingleChildScrollView(
      padding: EdgeInsets.all(20),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          _buildTipSection('Health Tips', healthTips, Icons.health_and_safety, Colors.red[300]!),
          SizedBox(height: 20),
          _buildTipSection('Environment Tips', environmentTips, Icons.eco, Colors.green[300]!),
          SizedBox(height: 20),
          _buildTipSection('Eco Tips', ecoTips, Icons.lightbulb, Colors.yellow[300]!),
        ],
      ),
    );
  }

  Widget _buildTipSection(String title, List<String> tips, IconData icon, Color color) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          title,
          style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
        ),
        SizedBox(height: 10),
        ...tips.map((tip) => 
          ListTile(
            leading: Icon(icon, color: color),
            title: Text(tip),
          )
        ).toList(),
      ],
    );
  }
}

// Chart Data Class
class ChartData {
  ChartData(this.category, this.value);
  final String category;
  final double value;
}

// Stat Row Data Class
class StatRowData {
  StatRowData(this.name, this.value);
  final String name;
  final int value;
}

// Type Defense Chip Data Class
class TypeDefenseChipData {
  TypeDefenseChipData(this.type, this.multiplier);
  final String type;
  final String multiplier;
}

// Stat Row Widget
class StatRow extends StatelessWidget {
  final String statName;
  final int statValue;

  StatRow({required this.statName, required this.statValue});

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 8.0),
      child: Row(
        children: [
          SizedBox(
            width: 60,
            child: Text(
              statName,
              style: TextStyle(fontSize: 16),
            ),
          ),
          SizedBox(width: 16),
          Expanded(
            child: SizedBox(
              height: 10,
              child: ClipRRect(
                borderRadius: BorderRadius.circular(5),
                child: LinearProgressIndicator(
                  value: statValue / 100,
                  backgroundColor: Colors.grey[300],
                  valueColor: AlwaysStoppedAnimation<Color>(Color(0xFFFB6C6C)),
                ),
              ),
            ),
          ),
          SizedBox(width: 16),
          Text(
            statValue.toString(),
            style: TextStyle(fontSize: 16),
          ),
        ],
      ),
    );
  }
}

// Type Defense Chip Widget
class TypeDefenseChip extends StatelessWidget {
  final String type;
  final String multiplier;
  final Color? backgroundColor;

  TypeDefenseChip(
      {required this.type, required this.multiplier, this.backgroundColor});

  @override
  Widget build(BuildContext context) {
    Color chipBackgroundColor = backgroundColor ?? Colors.grey; // Default color
    switch (type) {
      case 'Grass':
        chipBackgroundColor = Color(0xFF78C850);
        break;
      case 'Calories: High':
        chipBackgroundColor = Color(0xFFF08030);
        break;
      case 'Fire':
        chipBackgroundColor = Color(0xFFF08030);
        break;
      case 'Flying':
        chipBackgroundColor = Color(0xFFA890F0);
        break;
      case 'Water':
        chipBackgroundColor = Color(0xFF6890F0);
        break;
      case 'Bug':
        chipBackgroundColor = Color(0xFFA8B820);
        break;
      case 'Normal':
        chipBackgroundColor = Color(0xFFA8A878);
        break;
      case 'Electric':
        chipBackgroundColor = Color(0xFFF8D030);
        break;
      case 'Ground':
        chipBackgroundColor = Color(0xFFE0C068);
        break;
      case 'Fairy':
        chipBackgroundColor = Color(0xFFEE99AC);
        break;
      case 'Fighting':
        chipBackgroundColor = Color(0xFFC03028);
        break;
      case 'Psychic':
        chipBackgroundColor = Color(0xFFF85888);
        break;
      case 'Rock':
        chipBackgroundColor = Color(0xFFB8A038);
        break;
    }

    return Container(
      padding: EdgeInsets.symmetric(horizontal: 12, vertical: 6),
      decoration: BoxDecoration(
        color: chipBackgroundColor.withOpacity(0.4),
        borderRadius: BorderRadius.circular(20),
      ),
      child: Text(
        '$type $multiplier',
        style: TextStyle(
          color: Colors.black,
          fontWeight: FontWeight.bold,
          fontSize: 14,
        ),
      ),
    );
  }
}

// Evolution Tab Widget
class EvolutionTab extends StatelessWidget {
  final List<EvolutionStageData> evolutionStages;

  EvolutionTab({required this.evolutionStages});

  @override
  Widget build(BuildContext context) {
    return SingleChildScrollView(
      padding: EdgeInsets.all(20),
      child: Column(
        children: [
          Text(
            'Evolution Chain',
            style: TextStyle(
              fontSize: 20,
              fontWeight: FontWeight.bold,
            ),
          ),
          SizedBox(height: 20),
          ..._buildEvolutionChain(evolutionStages),
        ],
      ),
    );
  }

  List<Widget> _buildEvolutionChain(List<EvolutionStageData> stages) {
    List<Widget> chain = [];
    for (int i = 0; i < stages.length; i++) {
      chain.add(EvolutionStage(
          imageUrl: stages[i].imageUrl, name: stages[i].name));
      if (i < stages.length - 1) {
        chain.add(Icon(Icons.arrow_forward, size: 30));
      }
    }
    return [Row(mainAxisAlignment: MainAxisAlignment.spaceAround, children: chain)];
  }
}

// Evolution Stage Data Class
class EvolutionStageData {
  EvolutionStageData(this.imageUrl, this.name);
  final String imageUrl;
  final String name;
}

// Evolution Stage Widget
class EvolutionStage extends StatelessWidget {
  final String imageUrl;
  final String name;

  EvolutionStage({required this.imageUrl, required this.name});

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        Image.network(
          imageUrl,
          width: 80,
          height: 80,
        ),
        SizedBox(height: 8),
        Text(
          name,
          style: TextStyle(fontWeight: FontWeight.bold),
        ),
      ],
    );
  }
}

// Moves Tab Widget
class MovesTab extends StatelessWidget {
  final String moveListTitle;
  final List<MoveTileData> moves;

  MovesTab({required this.moveListTitle, required this.moves});

  @override
  Widget build(BuildContext context) {
    return SingleChildScrollView(
      padding: EdgeInsets.all(20),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            moveListTitle,
            style: TextStyle(fontWeight: FontWeight.bold, fontSize: 18),
          ),
          SizedBox(height: 10),
          ...moves
              .map((move) => MoveTile(moveName: move.name, level: move.level))
              .toList(),
        ],
      ),
    );
  }
}

// Move Tile Data Class
class MoveTileData {
  MoveTileData(this.name, this.level);
  final String name;
  final String level;
}

// Move Tile Widget
class MoveTile extends StatelessWidget {
  final String moveName;
  final String level;

  MoveTile({required this.moveName, required this.level});

  @override
  Widget build(BuildContext context) {
    return ListTile(
      title: Text(moveName),
      trailing: Text('Lv. $level'),
    );
  }
}