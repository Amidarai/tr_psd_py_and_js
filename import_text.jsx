// Функция для парсинга JSON вручную (если JSON не поддерживается)
if (typeof JSON === "undefined") {
  var JSON = {
    parse: function (str) {
      return eval("(" + str + ")");
    },
    stringify: function (obj) {
      var t = typeof obj;
      if (t == "object" && obj !== null) {
        if (Array.isArray(obj)) {
          var res = "[";
          for (var i = 0; i < obj.length; i++) {
            if (i > 0) res += ",";
            res += JSON.stringify(obj[i]);
          }
          res += "]";
          return res;
        } else {
          var res = "{";
          for (var key in obj) {
            if (obj.hasOwnProperty(key)) {
              if (res.length > 1) res += ",";
              res += JSON.stringify(key) + ":" + JSON.stringify(obj[key]);
            }
          }
          res += "}";
          return res;
        }
      }
      return '"' + obj + '"';
    },
  };
}

// Получаем путь к папке с текущим скриптом
var scriptFolder = new Folder($.fileName).parent;
// Путь к папке "Output"
var outputFolder = new Folder(scriptFolder + "/Output");
// Указываем имя файла, который ищем
var fileName = "translated_text.json"; // Укажите имя файла, который нужно найти
var filePath = outputFolder + "/" + fileName;

// Открытие переведенного текста из JSON
var translations = {}; // Сюда загрузим JSON с переведенным текстом

// Функция для загрузки переведенного текста
function loadTranslations() {
  var file = new File(filePath); // Путь к вашему JSON файлу
  if (file.exists) {
    file.open("r");
    var content = file.read();
    translations = JSON.parse(content); // Загружаем JSON
    file.close();
  } else {
    alert("Файл с переводом не найден!");
  }
}

// Функция для замены текста в слоях
function replaceTextInLayers(layers) {
  for (var i = 0; i < layers.length; i++) {
    var layer = layers[i];

    if (layer.kind == LayerKind.TEXT) {
      var originalText = layer.textItem.contents;
      // Если текст найден в переводах, заменяем его
      if (translations[originalText]) {
        layer.textItem.contents = translations[originalText];
      }
    }

    // Если это группа слоев, рекурсивно обрабатываем её слои
    if (layer.typename === "LayerSet") {
      replaceTextInLayers(layer.layers);
    }
  }
}

// Основная функция
function main() {
  loadTranslations(); // Загружаем переведенный текст
  var doc = app.activeDocument;
  var layers = doc.layers;
  replaceTextInLayers(layers); // Заменяем текст в слоях
  alert("Текстовые слои обновлены!");
}

// Проверяем, существует ли папка "Output"
if (!outputFolder.exists) {
  alert('Папка "Output" не существует.');
} else {
  // Проверяем, существует ли файл в папке "Output"
  var file = new File(filePath);
  if (!file.exists) {
    alert('Файл "' + fileName + '" не найден в папке "Output".');
  } else {
    // Запуск скрипта
    main();
  }
}
