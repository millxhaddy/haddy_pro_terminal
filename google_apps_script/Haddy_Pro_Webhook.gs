/**
 * Haddy Pro Google Sheets Webhook.
 * Deploy as a Web App executing as the spreadsheet owner.
 * Configure HADDY_WEBHOOK_TOKEN in Apps Script Script Properties.
 */

const WEBHOOK_VERSION = "4.6";
const MAX_BATCH_ITEMS = 100;
const MAX_ROW_COLUMNS = 100;
const MAX_CELL_UPDATES = 100;

const OFFICIAL_TABS = {
  pusat_kawalan: "00_Pusat Kawalan",
  meja_keputusan: "01_Meja Keputusan",
  pegangan_semasa: "02_Pegangan Semasa",
  jurnal_dagangan: "03_Jurnal Dagangan",
  senarai_pantau: "04_Senarai Pantau",
  kalkulator_3m: "05_Kalkulator 3M",
  pangkalan_1000: "06_Pangkalan 1000",
  lejar_liabiliti: "10_Lejar Liabiliti",
  skor_kredit: "11_Skor Kredit",
  program_akpk: "12_Program AKPK",
  sewa_beli_kereta: "13_Sewa Beli Kereta",
  pinjaman_cimb: "14_Pinjaman CIMB",
  kad_kredit_rhb: "15_Kad Kredit RHB",
  radar_makro: "31_Radar Makro",
  sejarah_dana: "40_Sejarah Dana",
  sejarah_padanan: "41_Sejarah Padanan",
  pantauan_pasaran: "60_Pantauan Pasaran",
  semua_saham: "61_Semua Saham",
  terminal_saham: "62_Terminal Saham",
  ringkasan_mudah: "63_Ringkasan Mudah",
  sistem_ddnk: "64_Sistem DDNK",
  sistem_dagangan_pro: "65_Sistem Dagangan Pro",
  aliran_tunai: "66_Aliran Tunai",
  moomoo_rekod: "67_Moomoo Rekod",
  cache_fundamental: "70_Cache Fundamental",
  cache_ohlcv: "71_Cache OHLCV",
  cache_earnings: "72_Cache Earnings",
  konfigurasi_sistem: "90_Konfigurasi Sistem",
  kesihatan_sistem: "91_Kesihatan Sistem"
};

// Keep header rows consistent with engine_gsheets.py.
const TAB_SCHEMAS = {
  "00_Pusat Kawalan": { headerRow: 5, keyCol: 3 },
  "01_Meja Keputusan": { headerRow: 4, keyCol: 2 },
  "02_Pegangan Semasa": { headerRow: 1, keyCol: 1 },
  "03_Jurnal Dagangan": { headerRow: 2, keyCol: 2 },
  "04_Senarai Pantau": { headerRow: 1, keyCol: 2 },
  "05_Kalkulator 3M": { headerRow: 1, keyCol: 1 },
  "06_Pangkalan 1000": { headerRow: 7, keyCol: 1 },
  "10_Lejar Liabiliti": { headerRow: 1, keyCol: 1 },
  "11_Skor Kredit": { headerRow: 13, keyCol: 1 },
  "12_Program AKPK": { headerRow: 1, keyCol: 4 },
  "13_Sewa Beli Kereta": { headerRow: 1, keyCol: 1 },
  "14_Pinjaman CIMB": { headerRow: 6, keyCol: 1 },
  "15_Kad Kredit RHB": { headerRow: 8, keyCol: 1 },
  "66_Aliran Tunai": { headerRow: 2, keyCol: 1 }
};

const WRITE_ALLOWED_TABS = {
  "02_Pegangan Semasa": true,
  "03_Jurnal Dagangan": true,
  "04_Senarai Pantau": true,
  "05_Kalkulator 3M": true,
  "12_Program AKPK": true
};

function verifyRequestAuth_(payload, e) {
  const expected = PropertiesService.getScriptProperties()
    .getProperty("HADDY_WEBHOOK_TOKEN");
  if (!expected || String(expected).trim().length < 32) return false;

  const bodyToken = payload &&
    (payload.token || payload.api_key || payload.secret);
  const queryToken = e && e.parameter &&
    (e.parameter.token || e.parameter.api_key);
  const provided = String(bodyToken || queryToken || "").trim();
  return constantTimeEqual_(String(expected).trim(), provided);
}

function constantTimeEqual_(expected, provided) {
  const maxLength = Math.max(expected.length, provided.length);
  let difference = expected.length ^ provided.length;
  for (let i = 0; i < maxLength; i++) {
    difference |= (expected.charCodeAt(i) || 0) ^
      (provided.charCodeAt(i) || 0);
  }
  return difference === 0;
}

function resolveSheet_(ss, tabIdentifier) {
  if (!tabIdentifier) return ss.getSheetByName("00_Pusat Kawalan");
  const cleanId = String(tabIdentifier).trim();
  const mappedName = OFFICIAL_TABS[cleanId.toLowerCase()] || cleanId;
  const directMatch = ss.getSheetByName(mappedName);
  if (directMatch) return directMatch;

  const normalizedTarget = mappedName.toLowerCase().replace(/[\s_]+/g, "");
  const sheets = ss.getSheets();
  for (let i = 0; i < sheets.length; i++) {
    const normalizedName = sheets[i].getName()
      .toLowerCase().replace(/[\s_]+/g, "");
    if (normalizedName === normalizedTarget) return sheets[i];
  }
  return null;
}

function doGet(e) {
  const startMs = Date.now();
  try {
    if (!verifyRequestAuth_(null, e)) {
      return jsonResponse_({ status: "error", code: "unauthorized" });
    }

    const ss = SpreadsheetApp.getActiveSpreadsheet();
    if (!ss) throw new Error("active_spreadsheet_unavailable");
    const params = e && e.parameter ? e.parameter : {};
    const action = String(params.action || "get_all").toLowerCase();
    const tabParam = String(params.tab || "");

    if (action === "ping") {
      return jsonResponse_({
        status: "ok",
        engine: "Haddy Pro Webhook " + WEBHOOK_VERSION,
        timestamp: new Date().toISOString(),
        latency_ms: Date.now() - startMs
      });
    }

    if (action === "get_tab" || tabParam) {
      try {
        const sheet = resolveSheet_(ss, tabParam || "00_Pusat Kawalan");
        if (!sheet) {
          return jsonResponse_({ status: "error", code: "tab_not_found" });
        }
        return jsonResponse_({
          status: "ok",
          tab: sheet.getName(),
          data: extractSheetData_(sheet),
          timestamp: new Date().toISOString()
        });
      } catch (err) {
        Logger.log("Could not read requested tab");
        return jsonResponse_({
          status: "error",
          code: "tab_read_failed"
        });
      }
    }

    if (action !== "get_all") {
      return jsonResponse_({ status: "error", code: "unsupported_action" });
    }

    const vault = {};
    const failedTabs = [];
    const missingTabs = [];
    Object.keys(OFFICIAL_TABS).forEach(function(alias) {
      const tabName = OFFICIAL_TABS[alias];
      try {
        const sheet = ss.getSheetByName(tabName);
        if (!sheet) {
          missingTabs.push(tabName);
          return;
        }
        vault[tabName] = extractSheetData_(sheet);
      } catch (err) {
        failedTabs.push(tabName);
        Logger.log("Could not read tab: " + tabName);
      }
    });

    if (!Object.keys(vault).length) {
      return jsonResponse_({
        status: "error",
        code: "no_tabs_readable",
        failed_tabs: failedTabs,
        timestamp: new Date().toISOString()
      });
    }

    return jsonResponse_({
      status: "ok",
      timestamp: new Date().toISOString(),
      latency_ms: Date.now() - startMs,
      tabs_count: Object.keys(vault).length,
      failed_tabs: failedTabs,
      missing_tabs: missingTabs,
      vault: vault
    });
  } catch (err) {
    Logger.log("doGet failed");
    return jsonResponse_({ status: "error", code: "server_error" });
  }
}

function doPost(e) {
  let lockAcquired = false;
  let lock = null;
  try {
    const rawBody = e && e.postData && e.postData.contents
      ? e.postData.contents
      : "{}";
    const payload = JSON.parse(rawBody);
    if (!payload || typeof payload !== "object" || Array.isArray(payload)) {
      return jsonResponse_({ status: "error", code: "invalid_payload" });
    }
    if (!verifyRequestAuth_(payload, e)) {
      return jsonResponse_({ status: "error", code: "unauthorized" });
    }

    lock = LockService.getScriptLock();
    lockAcquired = lock.tryLock(15000);
    if (!lockAcquired) {
      return jsonResponse_({ status: "error", code: "busy" });
    }

    const ss = SpreadsheetApp.getActiveSpreadsheet();
    if (!ss) throw new Error("active_spreadsheet_unavailable");
    const action = String(payload.action || "upsert_row").toLowerCase();

    if (action === "batch_sync") {
      if (!Array.isArray(payload.items) ||
          payload.items.length === 0 ||
          payload.items.length > MAX_BATCH_ITEMS) {
        return jsonResponse_({ status: "error", code: "invalid_batch_size" });
      }
      const results = payload.items.map(function(item) {
        try {
          return processSingleOperation_(ss, item);
        } catch (err) {
          Logger.log("Batch item failed");
          return { status: "error", reason: "operation_failed" };
        }
      });
      SpreadsheetApp.flush();
      updateLastSyncTimestamp_(ss);
      return jsonResponse_({
        status: "ok",
        synced_count: results.filter(function(result) {
          return result.status !== "error" && result.status !== "skipped";
        }).length,
        results: results,
        timestamp: new Date().toISOString()
      });
    }

    const result = processSingleOperation_(ss, payload);
    if (result.status === "error" || result.status === "skipped") {
      return jsonResponse_({ status: "error", result: result });
    }
    SpreadsheetApp.flush();
    updateLastSyncTimestamp_(ss);
    return jsonResponse_({
      status: "ok",
      result: result,
      timestamp: new Date().toISOString()
    });
  } catch (err) {
    Logger.log("doPost failed");
    return jsonResponse_({ status: "error", code: "server_error" });
  } finally {
    if (lockAcquired) lock.releaseLock();
  }
}

function processSingleOperation_(ss, item) {
  if (!item || typeof item !== "object" || Array.isArray(item)) {
    return { status: "error", reason: "invalid_item" };
  }
  const action = String(item.action || "upsert_row").toLowerCase();
  const targetName = item.tab || item.sheet || routeDefaultTab_(action);
  const sheet = resolveSheet_(ss, targetName);
  if (!sheet) return { status: "skipped", reason: "tab_not_found" };

  const sheetName = sheet.getName();
  if (!WRITE_ALLOWED_TABS[sheetName]) {
    return { status: "skipped", reason: "write_not_allowed" };
  }
  const schema = TAB_SCHEMAS[sheetName] || { headerRow: 1, keyCol: 1 };

  if (action === "update_3m") {
    if (sheetName !== "05_Kalkulator 3M") {
      return { status: "skipped", reason: "invalid_target" };
    }
    const fields = {
      ticker: ["C1", function(value) {
        return safeText_(String(value).toUpperCase().trim());
      }],
      max_risk_rm: ["C2", numberValue_],
      entry_price: ["C3", numberValue_],
      stop_loss: ["C4", numberValue_],
      take_profit: ["C5", numberValue_],
      market_type: ["C6", function(value) {
        return safeText_(String(value));
      }],
      gross_capital: ["C7", numberValue_]
    };
    const updates = [];
    Object.keys(fields).forEach(function(key) {
      if (item[key] !== undefined) {
        const field = fields[key];
        updates.push([field[0], field[1](item[key])]);
      }
    });
    if (!updates.length) return { status: "error", reason: "empty_update" };
    updates.forEach(function(update) {
      sheet.getRange(update[0]).setValue(update[1]);
    });
    return { status: "updated_3m", tab: sheetName };
  }

  if (action === "update_cells") {
    if (sheetName !== "05_Kalkulator 3M" ||
        !item.cells ||
        typeof item.cells !== "object" ||
        Array.isArray(item.cells)) {
      return { status: "skipped", reason: "invalid_cell_update" };
    }
    const cellKeys = Object.keys(item.cells);
    if (!cellKeys.length || cellKeys.length > MAX_CELL_UPDATES ||
        cellKeys.some(function(cell) { return !/^C[1-7]$/.test(cell); })) {
      return { status: "error", reason: "invalid_cell_range" };
    }
    cellKeys.forEach(function(cell) {
      sheet.getRange(cell).setValue(sanitizeCellValue_(item.cells[cell]));
    });
    return { status: "cells_updated", tab: sheetName, count: cellKeys.length };
  }

  if (!["append_row", "log_trade", "log_payment", "upsert_row"].includes(action)) {
    return { status: "error", reason: "unsupported_action" };
  }
  const rowData = item.row || item.data || item.values;
  const headers = getCleanHeaders_(sheet, schema.headerRow);
  const row = normalizeToRowArray_(rowData, headers);
  if (!row.length || row.length > MAX_ROW_COLUMNS) {
    return { status: "error", reason: "invalid_row_size" };
  }
  const safeRow = row.map(sanitizeCellValue_);

  if (["append_row", "log_trade", "log_payment"].includes(action)) {
    const nextRow = Math.max(sheet.getLastRow() + 1, schema.headerRow + 1);
    sheet.getRange(nextRow, 1, 1, safeRow.length).setValues([safeRow]);
    return { status: "appended", tab: sheetName, row: nextRow };
  }

  const keyColumn = Number(item.key_col || schema.keyCol || 1);
  if (!Number.isInteger(keyColumn) || keyColumn < 1 ||
      keyColumn > safeRow.length) {
    return { status: "error", reason: "invalid_key_column" };
  }
  const rawKey = item.key_value !== undefined
    ? item.key_value
    : safeRow[keyColumn - 1];
  const key = String(rawKey || "").trim().toUpperCase();
  if (key) {
    const lastRow = sheet.getLastRow();
    if (lastRow > schema.headerRow) {
      const numRows = lastRow - schema.headerRow;
      const keys = sheet.getRange(
        schema.headerRow + 1, keyColumn, numRows, 1
      ).getDisplayValues();
      for (let i = 0; i < keys.length; i++) {
        if (String(keys[i][0]).trim().toUpperCase() === key) {
          const targetRow = schema.headerRow + 1 + i;
          sheet.getRange(targetRow, 1, 1, safeRow.length)
            .setValues([safeRow]);
          return { status: "updated", tab: sheetName, row: targetRow };
        }
      }
    }
  }
  const newRow = Math.max(sheet.getLastRow() + 1, schema.headerRow + 1);
  sheet.getRange(newRow, 1, 1, safeRow.length).setValues([safeRow]);
  return { status: "inserted", tab: sheetName };
}

function numberValue_(value) {
  if (value === null || value === undefined ||
      typeof value === "boolean" ||
      (typeof value === "string" && !value.trim())) {
    throw new Error("invalid_number");
  }
  const number = Number(value);
  if (!Number.isFinite(number)) throw new Error("invalid_number");
  return number;
}

function safeText_(value) {
  return /^\s*[=+\-@]/.test(value) ? "'" + value : value;
}

function sanitizeCellValue_(value) {
  return typeof value === "string" ? safeText_(value) : value;
}

function extractSheetData_(sheet) {
  // Keep formula error text visible so the client can identify invalid data.
  return sheet.getDataRange().getDisplayValues();
}

function getCleanHeaders_(sheet, headerRow) {
  const lastColumn = Math.max(1, sheet.getLastColumn());
  return sheet.getRange(headerRow, 1, 1, lastColumn).getDisplayValues()[0];
}

function normalizeToRowArray_(rowData, headers) {
  if (Array.isArray(rowData)) return rowData;
  if (rowData && typeof rowData === "object") {
    return headers.map(function(header) {
      const cleanHeader = String(header).trim();
      if (rowData[cleanHeader] !== undefined) return rowData[cleanHeader];
      const normalizedHeader = cleanHeader
        .replace(/[^a-zA-Z0-9\s]/g, "").trim().toLowerCase();
      const matchedKey = Object.keys(rowData).find(function(key) {
        return key.replace(/[^a-zA-Z0-9\s]/g, "")
          .trim().toLowerCase() === normalizedHeader;
      });
      return matchedKey ? rowData[matchedKey] : "";
    });
  }
  return rowData === undefined || rowData === null ? [] : [rowData];
}

function routeDefaultTab_(action) {
  if (action === "log_trade") return "03_Jurnal Dagangan";
  if (action === "update_3m") return "05_Kalkulator 3M";
  if (action === "log_payment") return "12_Program AKPK";
  return "02_Pegangan Semasa";
}

function updateLastSyncTimestamp_(ss) {
  const systemSheet = ss.getSheetByName("91_Kesihatan Sistem");
  if (!systemSheet) return;
  try {
    systemSheet.getRange("B2").setValue(
      Utilities.formatDate(
        new Date(),
        "Asia/Kuala_Lumpur",
        "yyyy-MM-dd HH:mm:ss"
      )
    );
  } catch (err) {
    Logger.log("Could not update sync timestamp");
  }
}

function jsonResponse_(object) {
  return ContentService
    .createTextOutput(JSON.stringify(object))
    .setMimeType(ContentService.MimeType.JSON);
}
