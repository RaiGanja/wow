-- Saves equipment up to level 30 from the client (addon API: GetItemInfoInstant, GetItemInfo, GetItemStats, the item tooltip)
-- and where items come from while you play: dungeon boss loot, quest rewards, recipes of an open profession window.
-- /ggd scan            scans item ids 1-30000 and 200000-300000 (about a minute; stay in a city, nothing is sent anywhere)
-- /ggd scan A B        scans ids A-B
-- /ggd                 shows what is saved
-- Log out to write WTF/Account/<account>/SavedVariables/GabellaGear.lua -> python tools/gear_import.py --addon <file>
GabellaGearDB = GabellaGearDB or {}

local MAXREQ, STEP, TICK = 30, 60, 0.25
local SKIP = { INVTYPE_BODY = true, INVTYPE_TABARD = true, INVTYPE_BAG = true, INVTYPE_AMMO = true, INVTYPE_QUIVER = true,
               INVTYPE_RELIC = true, INVTYPE_NON_EQUIP_IGNORE = true }
local tip = CreateFrame("GameTooltip", "GabellaGearTip", nil, "GameTooltipTemplate")
tip:SetOwner(WorldFrame, "ANCHOR_NONE")
local getStats = (C_Item and C_Item.GetItemStats) or GetItemStats
local request = C_Item and C_Item.RequestLoadItemDataByID

local function db()
  GabellaGearDB.items = GabellaGearDB.items or {}
  GabellaGearDB.src = GabellaGearDB.src or {}
  GabellaGearDB.build = select(1, GetBuildInfo()) .. "." .. select(2, GetBuildInfo())
  return GabellaGearDB
end

local function tipLines(link)
  tip:ClearLines()
  tip:SetHyperlink(link)
  local out = {}
  for i = 1, tip:NumLines() do
    local l = _G["GabellaGearTipTextLeft" .. i]
    local t = l and l:GetText()
    if t and t ~= "" then out[#out + 1] = t end
  end
  return out
end

local function save(id)
  local name, link, q, ilvl, req, _, _, _, equip, icon, _, cls, sub = GetItemInfo(id)
  if not name or not equip or equip == "" or SKIP[equip] or (req or 0) > MAXREQ or (q or 0) < 1 then return false end
  local d, loc = db(), GetLocale()
  local it = d.items[id] or { name = {}, tip = {} }
  it.name[loc] = name
  it.slot, it.ilvl, it.req, it.q, it.icon, it.cls, it.sub = equip, ilvl, req, q, icon, cls, sub
  it.stats = getStats(link) or {}
  it.tip[loc] = tipLines(link)
  d.items[id] = it
  return true
end

local function itemId(link)
  return link and tonumber(link:match("item:(%d+)"))
end

local function addSrc(id, key, rec)
  if not id then return end
  local d = db()
  d.src[id] = d.src[id] or {}
  local loc, old = GetLocale(), d.src[id][key]
  if old then
    for _, f in ipairs({ "name", "zone" }) do
      if rec[f] then old[f] = old[f] or {}; old[f][loc] = rec[f][loc] end
    end
  else
    d.src[id][key] = rec
  end
  if not save(id) and request then request(id) end
end

-- scan: ask the client for every id in the ranges, a few at a time; GET_ITEM_INFO_RECEIVED saves the ones it had to load
local queue, pos, ticker, found = {}, 0, nil, 0

local function step()
  for _ = 1, STEP do
    pos = pos + 1
    local r = queue[1]
    if not r then ticker:Cancel(); ticker = nil
      print("|cffc9a54aGabella|r: scan done, " .. found .. " items. Log out to write the file."); return end
    local id = r[1] + r.n
    r.n = r.n + 1
    if id > r[2] then table.remove(queue, 1) else
      local _, _, _, equip = GetItemInfoInstant(id)
      if equip and equip ~= "" and not SKIP[equip] then
        if save(id) then found = found + 1 elseif request then request(id) end
      end
    end
  end
end

local f = CreateFrame("Frame")
f:RegisterEvent("GET_ITEM_INFO_RECEIVED")
f:RegisterEvent("LOOT_READY")
f:RegisterEvent("QUEST_DETAIL")
f:RegisterEvent("QUEST_COMPLETE")
f:RegisterEvent("TRADE_SKILL_SHOW")
f:SetScript("OnEvent", function(_, ev, a1, a2)
  local loc = GetLocale()
  if ev == "GET_ITEM_INFO_RECEIVED" then
    if a2 and save(a1) then found = found + 1 end
  elseif ev == "LOOT_READY" then                                   -- a dungeon boss: the corpse you loot is your target
    local zone, kind = GetInstanceInfo()
    if kind ~= "party" then return end
    local guid = UnitGUID("target")
    if not guid or not UnitIsDead("target") then return end
    local npc = select(6, strsplit("-", guid))
    for s = 1, GetNumLootItems() do
      addSrc(itemId(GetLootSlotLink(s)), "drop:" .. tostring(npc),
             { kind = "drop", npc = tonumber(npc), name = { [loc] = UnitName("target") }, zone = { [loc] = zone } })
    end
  elseif ev == "QUEST_DETAIL" or ev == "QUEST_COMPLETE" then       -- the rewards of the quest window, with your faction
    local qid, title = GetQuestID and GetQuestID() or 0, GetTitleText()
    local rec = function() return { kind = "quest", quest = qid, name = { [loc] = title }, faction = (UnitFactionGroup("player")) } end
    for i = 1, GetNumQuestChoices() do addSrc(itemId(GetQuestItemLink("choice", i)), "quest:" .. qid, rec()) end
    for i = 1, GetNumQuestRewards() do addSrc(itemId(GetQuestItemLink("reward", i)), "quest:" .. qid, rec()) end
  elseif ev == "TRADE_SKILL_SHOW" then                             -- what the open profession window makes
    local prof = GetTradeSkillLine()
    for i = 1, GetNumTradeSkills() do
      local _, kind = GetTradeSkillInfo(i)
      if kind ~= "header" then
        addSrc(itemId(GetTradeSkillItemLink(i)), "craft:" .. tostring(prof), { kind = "craft", name = { [loc] = prof } })
      end
    end
  end
end)

SLASH_GABELLAGEAR1 = "/ggd"
SlashCmdList.GABELLAGEAR = function(msg)
  local a, b = (msg or ""):match("^scan%s*(%d*)%s*(%d*)")
  if a then
    queue, found = {}, 0
    if a ~= "" and b ~= "" then queue[1] = { tonumber(a), tonumber(b), n = 0 }
    else queue = { { 1, 30000, n = 0 }, { 200000, 300000, n = 0 } } end
    if not ticker then ticker = C_Timer.NewTicker(TICK, step) end
    print("|cffc9a54aGabella|r: scanning items (" .. GetLocale() .. ")...")
    return
  end
  local n, s = 0, 0
  for _ in pairs(db().items) do n = n + 1 end
  for _ in pairs(db().src) do s = s + 1 end
  print("|cffc9a54aGabella|r: " .. n .. " items, " .. s .. " with a source. /ggd scan to scan.")
end
