// Single source of truth for every fact on the page.
// Anything here must trace back to the product or the owners. Do not add claims that don't.

export const LINKS = {
  starterLaunch: "https://hamzaouiy4.gumroad.com/l/Soloandstarving/LAUNCH45?wanted=true",
  // Used automatically once the launch window closes. Confirm this URL with the owners.
  starterRegular: "https://hamzaouiy4.gumroad.com/l/Soloandstarving?wanted=true",
  custom: "https://hamzaouiy4.gumroad.com/l/dmcajy",
  email: "yndigitalbusiness@gmail.com",
  privacy: "https://soloandstarving.store/privacy",
} as const;

export const PRICING = {
  launchPrice: 19.25,
  regularPrice: 35,
  customPrice: 69,
  // Launch price ends at midnight New York time on October 1.
  launchEndsAt: "2026-10-01T00:00:00-04:00",
} as const;

export type Mode = "normal" | "tired" | "dead";

export const MODES: Record<Mode, { label: string; minutes: number; line: string }> = {
  normal: { label: "Normal", minutes: 30, line: "You have a bit left in the tank. Real cooking, still under 30 minutes." },
  tired: { label: "Tired", minutes: 20, line: "Long day. One pan, short prep, dinner in 20." },
  dead: { label: "Dead tired", minutes: 10, line: "Barely standing. Ten minutes, almost no cooking, still a real meal." },
};

export type Recipe = {
  slug: string;
  name: string;
  cuisine: string;
  number?: number;
  image: string;
  width: number;
  height: number;
  minutes: number;
  cost: string;
  kcal: number;
  protein: number;
  mode: Mode;
  ingredients: string[];
  more: number;
  swaps: string;
};

export const RECIPES: Recipe[] = [
  {
    slug: "quesadillas",
    name: "Chicken Quesadillas",
    cuisine: "Mexican",
    number: 41,
    image: "/images/quesadilla.webp",
    width: 900,
    height: 1200,
    minutes: 15,
    cost: "$2.90",
    kcal: 525,
    protein: 51,
    mode: "tired",
    ingredients: ["300 g chicken (fresh or pre cooked)", "2 large tortillas", "75 g cheddar, shredded"],
    more: 3,
    swaps: "Chicken for ground turkey or chickpeas. Cheddar for mozzarella. Tortillas for pita or bread.",
  },
  {
    slug: "turkey-chili",
    name: "Turkey Chili",
    cuisine: "American",
    number: 49,
    image: "/images/turkey-chili.webp",
    width: 900,
    height: 1350,
    minutes: 25,
    cost: "$3.10",
    kcal: 475,
    protein: 43,
    mode: "normal",
    ingredients: ["300 g ground turkey", "1 can (400 g) kidney beans, drained", "1 can (400 g) chopped tomatoes"],
    more: 3,
    swaps: "Turkey for chicken or lean beef. Cheddar for mozzarella. Fresh onion for 1/2 tsp onion powder.",
  },
  {
    slug: "teriyaki-bowl",
    name: "Teriyaki Chicken Rice Bowl",
    cuisine: "Japanese",
    number: 55,
    image: "/images/teriyaki-bowl.webp",
    width: 900,
    height: 1200,
    minutes: 20,
    cost: "$2.75",
    kcal: 655,
    protein: 49,
    mode: "tired",
    ingredients: ["300 g chicken (fresh or pre cooked)", "2 tbsp soy sauce", "1 to 2 tbsp honey"],
    more: 5,
    swaps: "Chicken for ground turkey or chickpeas. Garlic for garlic powder. Rice for pasta, couscous or noodles.",
  },
  {
    slug: "fried-rice",
    name: "Chicken Fried Rice",
    cuisine: "Chinese",
    number: 61,
    image: "/images/fried-rice.webp",
    width: 900,
    height: 600,
    minutes: 15,
    cost: "$2.80",
    kcal: 720,
    protein: 61,
    mode: "tired",
    ingredients: ["300 g chicken (fresh or pre cooked)", "300 g cooked rice (or 150 g uncooked)", "4 eggs"],
    more: 4,
    swaps: "Chicken for ground turkey or chickpeas. Fresh garlic for garlic powder. Fresh onion for onion powder.",
  },
  {
    slug: "caprese-skillet",
    name: "Chicken Caprese Skillet",
    cuisine: "Italian",
    number: 67,
    image: "/images/caprese-skillet.webp",
    width: 900,
    height: 1200,
    minutes: 20,
    cost: "$2.90",
    kcal: 487,
    protein: 48,
    mode: "tired",
    ingredients: ["300 g chicken (fresh or pre cooked)", "75 g mozzarella, shredded", "1 handful cherry tomatoes, halved"],
    more: 3,
    swaps: "Chicken for ground turkey or chickpeas. Mozzarella for cheddar or provolone.",
  },
  {
    slug: "yogurt-crunch",
    name: "Greek Yogurt Chocolate Crunch",
    cuisine: "Dessert",
    image: "/images/yogurt-crunch.webp",
    width: 900,
    height: 750,
    minutes: 10,
    cost: "$1.35",
    kcal: 330,
    protein: 13,
    mode: "dead",
    ingredients: ["1/2 cup (120 g) Greek yogurt", "1 to 2 tbsp cocoa powder", "1 banana"],
    more: 2,
    swaps: "Greek yogurt for plain yogurt. Honey for maple syrup. Banana for any soft fruit like pear or mango.",
  },
];

// Which dish represents each mode in the hero switcher.
export const HERO_BY_MODE: Record<Mode, string> = {
  normal: "turkey-chili",
  tired: "caprese-skillet",
  dead: "yogurt-crunch",
};

export const RESEARCH = [
  {
    figure: "46%",
    label: "less food wasted",
    body: "US households that committed to one weekly \"Use-Up Day\", cooking from what was already in the fridge.",
    source: "Cooper et al. (2023), Resources, Conservation & Recycling",
  },
  {
    figure: "40,554",
    label: "adults studied",
    body: "People who planned meals ahead had better diets and lower odds of obesity than people who didn't.",
    source: "Ducrot et al. (2017), Int'l Journal of Behavioral Nutrition & Physical Activity",
  },
  {
    figure: "58.9%",
    label: "of US food spending goes to eating out",
    body: "In 2024, the highest share ever recorded. Most of that is the dinner nobody planned.",
    source: "USDA Economic Research Service, Food Expenditure Series (2024)",
  },
] as const;

export const FAQ = [
  {
    q: "I've genuinely never cooked. Will I manage?",
    a: "Yes. The book opens with a Start Here page for total beginners: heat levels, how to cook rice and pasta, and exactly when chicken is done. Every step is written like it's your first time, and most recipes use one pan.",
  },
  {
    q: "Are the recipes really for one person?",
    a: "Yes. Every recipe makes 2 portions for one person: dinner tonight and a second meal tomorrow. No scaling a family recipe down, no half an onion left over with nowhere to go.",
  },
  {
    q: "What exactly do I get?",
    a: "The interactive PDF cookbook with 88 recipes across 6 cuisines, plus two free bonuses: the Solo Meal Planner & Grocery Kit (4 pages) and 4 Week Dinner Plans with a shopping list for each week.",
  },
  {
    q: "Does it work on my phone?",
    a: "Yes. Open it in Adobe Acrobat Reader or your phone's built in PDF or Files app to tap from the recipe index straight to any meal. Some in browser previews won't let you tap, so use an app.",
  },
  {
    q: "How fast do I get the files?",
    a: "Instantly. Checkout runs through Gumroad, and the download link lands in your inbox the moment you pay. No account to create, nothing to install.",
  },
  {
    q: "How is this different from free recipes or asking ChatGPT?",
    a: "Free recipes are built for households, so you end up scaling down and guessing what to do with leftovers. Every recipe here is portioned for one from the start, tagged by energy level, and kept in one interactive PDF instead of ten open tabs.",
  },
  {
    q: "How do the Starter Bundle and Custom Plan differ?",
    a: "The Starter Bundle is instant: the full cookbook plus both bonuses. The Custom Plan includes all of that, then you fill in a short form with your preferences, allergies and schedule, and a real person builds your plan in 2 to 3 days. It can include a personal message page, which makes it a good gift.",
  },
  {
    q: "What if it's not right for me?",
    a: "Email us and a real person will make it right, whether that's help getting the file working, a swap, or in some cases another product on us. Because digital files are yours to keep the moment you download them, that's how we handle it instead of refunds.",
  },
] as const;
