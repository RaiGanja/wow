-- TEST DATA for tests/test_guides.py (shape of the GabellaGear SavedVariables), not a real dump
GabellaGearDB = {
	["build"] = "1.15.8.70500",
	["items"] = {
		[900101] = { ["name"] = { ["enUS"] = "Test Cloth Hood", ["ruRU"] = "Тестовый тканевый капюшон" }, ["slot"] = "INVTYPE_HEAD", ["ilvl"] = 25, ["req"] = 20, ["q"] = 2, ["cls"] = 4, ["sub"] = 1,
			["stats"] = { ["ITEM_MOD_INTELLECT_SHORT"] = 5, ["ITEM_MOD_SPIRIT_SHORT"] = 4, ["RESISTANCE0_NAME"] = 30 },
			["tip"] = { ["enUS"] = { "Test Cloth Hood", "Equip: Increases healing done by spells and effects by up to 9." } } },
		[900102] = { ["name"] = { ["enUS"] = "Test Plate Helm" }, ["slot"] = "INVTYPE_HEAD", ["ilvl"] = 28, ["req"] = 24, ["q"] = 3, ["cls"] = 4, ["sub"] = 4,
			["stats"] = { ["ITEM_MOD_STRENGTH_SHORT"] = 8, ["ITEM_MOD_STAMINA_SHORT"] = 8, ["RESISTANCE0_NAME"] = 300 } },
		[900103] = { ["name"] = { ["enUS"] = "Test Mail Coif" }, ["slot"] = "INVTYPE_HEAD", ["ilvl"] = 26, ["req"] = 21, ["q"] = 2, ["cls"] = 4, ["sub"] = 3,
			["stats"] = { ["ITEM_MOD_STRENGTH_SHORT"] = 5, ["ITEM_MOD_STAMINA_SHORT"] = 6, ["RESISTANCE0_NAME"] = 160 } },
		[900104] = { ["name"] = { ["enUS"] = "Test Low Cloth Cap" }, ["slot"] = "INVTYPE_HEAD", ["ilvl"] = 18, ["req"] = 13, ["q"] = 2, ["cls"] = 4, ["sub"] = 1,
			["stats"] = { ["ITEM_MOD_INTELLECT_SHORT"] = 2 } },
		[900105] = { ["name"] = { ["enUS"] = "Test Too High Robe" }, ["slot"] = "INVTYPE_ROBE", ["ilvl"] = 40, ["req"] = 35, ["q"] = 3, ["cls"] = 4, ["sub"] = 1,
			["stats"] = { ["ITEM_MOD_INTELLECT_SHORT"] = 12 } },
		[900106] = { ["name"] = { ["enUS"] = "Test Silk Gloves", ["ruRU"] = "Тестовые шёлковые перчатки" }, ["slot"] = "INVTYPE_HAND", ["ilvl"] = 24, ["req"] = 19, ["q"] = 2, ["cls"] = 4, ["sub"] = 1,
			["stats"] = { ["ITEM_MOD_INTELLECT_SHORT"] = 4, ["ITEM_MOD_SPIRIT_SHORT"] = 3 } },
	},
	["src"] = {
		[900101] = { ["drop:910001"] = { ["kind"] = "drop", ["npc"] = 910001, ["name"] = { ["enUS"] = "Test Boss" }, ["zone"] = { ["enUS"] = "Test Hollow" } } },
		[900103] = { ["quest:930001"] = { ["kind"] = "quest", ["quest"] = 930001, ["name"] = { ["enUS"] = "Test Quest" }, ["faction"] = "Horde" } },
		[900106] = { ["craft:Портняжное дело"] = { ["kind"] = "craft", ["name"] = { ["ruRU"] = "Портняжное дело" } } },
	},
}
