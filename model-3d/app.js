/* Model 3D gospodarstwa: teren z modelu GUGiK, strefy, obiekty projektu, Słońce i cień. */
(function () {
  'use strict';

  var F = window.FARM;
  var failEl = document.getElementById('fail');
  function fail(msg) { failEl.textContent = msg; failEl.hidden = false; }
  if (!F) { fail('Dane modelu nie wczytały się. Odśwież stronę.'); return; }
  if (!window.THREE || !THREE.OrbitControls) {
    fail('Biblioteka 3D nie wczytała się. Sprawdź połączenie z internetem i odśwież stronę.');
    return;
  }

  var M = F.meta, HALF = M.size / 2, n = M.n;
  var app = document.getElementById('app');
  var stage = document.getElementById('stage');
  var canvas = document.getElementById('scene');
  var labelsEl = document.getElementById('labels');
  function $(id) { return document.getElementById(id); }
  function cssVar(name) { return getComputedStyle(document.documentElement).getPropertyValue(name).trim(); }

  /* ---------- data decoding ---------- */
  function b64(s) { var bin = atob(s), u = new Uint8Array(bin.length); for (var i = 0; i < bin.length; i++) u[i] = bin.charCodeAt(i); return u; }
  function u16(s) { var b = b64(s); return new Uint16Array(b.buffer, 0, b.length >> 1); }
  function i16(s) { var b = b64(s); return new Int16Array(b.buffer, 0, b.length >> 1); }

  var H = u16(F.dtm);
  function hAt(r, c) { return H[r * n + c] / 100 + 100; }
  /* ground height [m n.p.m.] at local coordinates x = east, y = north [m from the window corner] */
  function ground(x, y) {
    var fc = (x - 1) / M.cell, fr = (M.size - 1 - y) / M.cell;
    fc = Math.min(Math.max(fc, 0), n - 1.001); fr = Math.min(Math.max(fr, 0), n - 1.001);
    var c = Math.floor(fc), r = Math.floor(fr), tx = fc - c, ty = fr - r;
    return (hAt(r, c) * (1 - tx) + hAt(r, c + 1) * tx) * (1 - ty) + (hAt(r + 1, c) * (1 - tx) + hAt(r + 1, c + 1) * tx) * ty;
  }
  function sx(x) { return x - HALF; }          /* east  -> scene X */
  function sz(y) { return HALF - y; }          /* north -> scene -Z */
  function sy(h) { return h - M.base; }        /* height above the lake level */
  function col(hex) { return new THREE.Color(hex).convertSRGBToLinear(); }

  /* ---------- renderer, camera, lights ---------- */
  var renderer;
  try { renderer = new THREE.WebGLRenderer({ canvas: canvas, antialias: true }); }
  catch (e) { fail('Ta przeglądarka nie obsługuje grafiki 3D (WebGL).'); return; }
  renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
  renderer.outputEncoding = THREE.sRGBEncoding;
  renderer.shadowMap.enabled = true;
  renderer.shadowMap.type = THREE.PCFSoftShadowMap;
  renderer.shadowMap.autoUpdate = false;

  var scene = new THREE.Scene();
  function applyTheme() { scene.background = new THREE.Color(cssVar('--sky') || '#cddbe1'); invalidate(); }

  var camera = new THREE.PerspectiveCamera(42, 1, 2, 5000);
  var controls = new THREE.OrbitControls(camera, canvas);
  controls.enableDamping = false;
  controls.maxPolarAngle = Math.PI / 2 - 0.02;
  controls.minDistance = 25;
  controls.maxDistance = 1200;
  controls.screenSpacePanning = false;

  var root = new THREE.Group();
  scene.add(root);

  var hemi = new THREE.HemisphereLight(0xffffff, 0x9aa08c, 0.78);
  scene.add(hemi);
  var sun = new THREE.DirectionalLight(0xfff1dc, 0.75);
  sun.castShadow = true;
  var mapSize = Math.min(2048, renderer.capabilities.maxTextureSize || 2048);
  sun.shadow.mapSize.set(mapSize, mapSize);
  var sc = sun.shadow.camera;
  sc.left = -270; sc.right = 270; sc.top = 270; sc.bottom = -270; sc.near = 10; sc.far = 1600;
  sc.updateProjectionMatrix();
  sun.shadow.bias = -0.0006;
  sun.shadow.normalBias = 0.6;
  sun.target.position.set(0, 6, 0);
  scene.add(sun);
  scene.add(sun.target);

  var dirty = true;
  function invalidate() { dirty = true; }
  function shadowsDirty() { renderer.shadowMap.needsUpdate = true; invalidate(); }

  /* ---------- terrain ---------- */
  var tgeo = new THREE.PlaneGeometry(M.size - M.cell, M.size - M.cell, n - 1, n - 1);
  tgeo.rotateX(-Math.PI / 2);
  (function () {
    var pos = tgeo.attributes.position, uv = tgeo.attributes.uv;
    for (var i = 0; i < n * n; i++) {
      var r = (i / n) | 0, c = i % n;
      pos.setY(i, sy(hAt(r, c)));
      uv.setXY(i, (1 + M.cell * c) / M.size, 1 - (1 + M.cell * r) / M.size);
    }
    tgeo.computeVertexNormals();
  })();

  var terrainMat = new THREE.MeshBasicMaterial({ color: col('#7d8f6a') });
  var terrain = new THREE.Mesh(tgeo, terrainMat);
  terrain.castShadow = true;
  root.add(terrain);

  (function () {
    var v = [], idx = [], base = -9, k = 0;
    function wall(get) {
      for (var i = 0; i < n; i++) { var p = get(i); v.push(p[0], p[1], p[2], p[0], base, p[2]); if (i > 0) { var q = k - 2; idx.push(q, q + 1, q + 2, q + 1, q + 3, q + 2); } k += 2; }
    }
    var e = (M.size - M.cell) / 2;
    wall(function (i) { return [-e + i * M.cell, sy(hAt(n - 1, i)), e]; });
    wall(function (i) { return [-e + i * M.cell, sy(hAt(0, i)), -e]; });
    wall(function (i) { return [-e, sy(hAt(i, 0)), -e + i * M.cell]; });
    wall(function (i) { return [e, sy(hAt(i, n - 1)), -e + i * M.cell]; });
    var g = new THREE.BufferGeometry();
    g.setAttribute('position', new THREE.Float32BufferAttribute(v, 3)); g.setIndex(idx);
    root.add(new THREE.Mesh(g, new THREE.MeshBasicMaterial({ color: col('#3b4a45'), side: THREE.DoubleSide })));
  })();

  function overlay(order) {
    var m = new THREE.MeshBasicMaterial({ transparent: true, depthWrite: false, polygonOffset: true, polygonOffsetFactor: -order, polygonOffsetUnits: -2 * order, visible: false });
    var mesh = new THREE.Mesh(tgeo, m);
    mesh.renderOrder = order;
    root.add(mesh);
    return mesh;
  }
  var zonesMesh = overlay(1), planMesh = overlay(2);
  var shadowMesh = new THREE.Mesh(tgeo, new THREE.ShadowMaterial({ opacity: 0.46, depthWrite: false, polygonOffset: true, polygonOffsetFactor: -3, polygonOffsetUnits: -6 }));
  shadowMesh.receiveShadow = true;
  shadowMesh.renderOrder = 3;
  root.add(shadowMesh);

  function loadTexture(url, done) {
    var img = new Image(), retried = false;
    img.onload = function () {
      var t = new THREE.Texture(img);
      t.encoding = THREE.sRGBEncoding;
      t.anisotropy = renderer.capabilities.getMaxAnisotropy();
      done(t);
      t.needsUpdate = true;
      invalidate();
    };
    img.onerror = function () { if (!retried) { retried = true; img.src = url; } };
    fetch(url).then(function (r) { if (!r.ok) throw new Error(String(r.status)); return r.blob(); })
      .then(function (b) { img.src = URL.createObjectURL(b); })
      .catch(function () { retried = true; img.src = url; });
  }
  loadTexture('orto.jpg', function (t) { terrainMat.map = t; terrainMat.color.set(0xffffff); terrainMat.needsUpdate = true; });
  function overlayTexture(mesh) {
    return function (t) {
      t.generateMipmaps = false; t.minFilter = THREE.LinearFilter;
      mesh.material.map = t; mesh.material.visible = true; mesh.material.needsUpdate = true;
    };
  }
  loadTexture('zones.png', overlayTexture(zonesMesh));
  loadTexture('plan.png', overlayTexture(planMesh));

  /* ---------- layer groups ---------- */
  var G = { obj: new THREE.Group(), plan: new THREE.Group(), trees: new THREE.Group(), s8a: new THREE.Group(), parcels: new THREE.Group() };
  Object.keys(G).forEach(function (k) { root.add(G[k]); });

  /* ---------- labels ---------- */
  var labels = [];
  function addLabel(text, x, y, h, cls, group, lift) {
    var el = document.createElement('div');
    el.className = 'lab ' + cls;
    el.textContent = text;
    labelsEl.appendChild(el);
    labels.push({ el: el, v: new THREE.Vector3(sx(x), sy(h) + (lift || 0), sz(y)), group: group });
  }
  var show = { zone: true, obj: true, field: true, map: true, all: true };
  var rank = { obj: 0, map: 1, zone: 2, field: 3 };
  var tmp = new THREE.Vector3(), sorted = null;
  /* labels are placed by priority; a label that would cover an already placed label stays hidden */
  function placeLabels() {
    var w = stage.clientWidth, h = stage.clientHeight, placed = [];
    if (!sorted || sorted.length !== labels.length) sorted = labels.slice().sort(function (a, b) { return rank[a.group] - rank[b.group]; });
    for (var i = 0; i < sorted.length; i++) {
      var L = sorted[i];
      if (!show.all || !show[L.group]) { L.el.style.display = 'none'; continue; }
      tmp.set(L.v.x, L.v.y * root.scale.y, L.v.z).project(camera);
      if (tmp.z < -1 || tmp.z > 1 || tmp.x < -1.05 || tmp.x > 1.05 || tmp.y < -1.05 || tmp.y > 1.05) { L.el.style.display = 'none'; continue; }
      var x = (tmp.x * 0.5 + 0.5) * w, y = (-tmp.y * 0.5 + 0.5) * h;
      if (!L.w) { L.el.style.display = ''; L.w = L.el.offsetWidth || 30; L.h = L.el.offsetHeight || 18; }
      var x0 = x - L.w / 2 - 3, x1 = x + L.w / 2 + 3, y0 = y - L.h / 2 - 2, y1 = y + L.h / 2 + 2, hit = false;
      for (var p = 0; p < placed.length; p++) { var q = placed[p]; if (x0 < q[2] && x1 > q[0] && y0 < q[3] && y1 > q[1]) { hit = true; break; } }
      if (hit) { L.el.style.display = 'none'; continue; }
      placed.push([x0, y0, x1, y1]);
      L.el.style.display = '';
      L.el.style.transform = 'translate(-50%,-50%) translate(' + x.toFixed(1) + 'px,' + y.toFixed(1) + 'px)';
    }
  }

  /* ---------- trees (measured tops and schematic stand) ---------- */
  function buildTrees(arr, count, group, colorA, colorB, opacity) {
    if (!count) return;
    var cone = new THREE.SphereGeometry(1, 7, 5);
    var trunkG = new THREE.CylinderGeometry(0.22, 0.3, 1, 5); trunkG.translate(0, 0.5, 0);
    var cm = new THREE.MeshLambertMaterial({ color: 0xffffff, transparent: opacity < 1, opacity: opacity });
    var tm = new THREE.MeshLambertMaterial({ color: col('#5b4632'), transparent: opacity < 1, opacity: opacity });
    var crowns = new THREE.InstancedMesh(cone, cm, count), trunks = new THREE.InstancedMesh(trunkG, tm, count);
    var d = new THREE.Object3D(), c = new THREE.Color(), a = col(colorA), b = col(colorB);
    for (var i = 0; i < count; i++) {
      var x = arr[3 * i] / 10, y = arr[3 * i + 1] / 10, h = arr[3 * i + 2] / 10;
      var g = sy(ground(x, y)), rad = Math.min(4.2, Math.max(1.2, 0.9 + 0.13 * h));
      d.position.set(sx(x), g + 0.62 * h, sz(y)); d.scale.set(rad, 0.38 * h, rad); d.rotation.set(0, (i * 2.399) % 6.283, 0); d.updateMatrix();
      crowns.setMatrixAt(i, d.matrix);
      c.copy(a).lerp(b, ((i * 7919) % 100) / 100); crowns.setColorAt(i, c);
      d.position.set(sx(x), g, sz(y)); d.scale.set(1, 0.32 * h, 1); d.rotation.set(0, 0, 0); d.updateMatrix();
      trunks.setMatrixAt(i, d.matrix);
    }
    crowns.instanceColor.needsUpdate = true;
    crowns.castShadow = true; crowns.frustumCulled = false; trunks.frustumCulled = false;
    group.add(crowns); group.add(trunks);
  }
  buildTrees(i16(F.trees), F.ntrees, G.trees, '#2f5d34', '#4f7f3f', 1);
  buildTrees(i16(F.sch), F.nsch, G.s8a, '#5c8c55', '#7aa66a', 0.85);

  /* ---------- buildings from the surface model ---------- */
  (function () {
    var a = i16(F.bld), N = F.nbld;
    if (!N) return;
    var box = new THREE.BoxGeometry(1, 1, 1); box.translate(0, 0.5, 0);
    var m = new THREE.InstancedMesh(box, new THREE.MeshLambertMaterial({ color: 0xffffff }), N);
    var d = new THREE.Object3D(), c = new THREE.Color();
    for (var i = 0; i < N; i++) {
      var x = a[6 * i] + 0.5, y = a[6 * i + 1] + 0.5, h = a[6 * i + 2] / 10, g = sy(ground(x, y));
      d.position.set(sx(x), g - 0.4, sz(y)); d.scale.set(1.02, h + 0.4, 1.02); d.updateMatrix();
      m.setMatrixAt(i, d.matrix);
      c.setRGB(a[6 * i + 3] / 255, a[6 * i + 4] / 255, a[6 * i + 5] / 255).convertSRGBToLinear();
      m.setColorAt(i, c);
    }
    m.instanceColor.needsUpdate = true;
    m.castShadow = true; m.receiveShadow = true; m.frustumCulled = false;
    G.trees.add(m);
  })();

  /* ---------- project objects ---------- */
  function lambert(hex, extra) { var p = { color: col(hex) }; if (extra) Object.keys(extra).forEach(function (k) { p[k] = extra[k]; }); return new THREE.MeshLambertMaterial(p); }
  function put(mesh, x, y, h, lift, group) {
    mesh.position.set(sx(x), sy(h) + (lift || 0), sz(y));
    mesh.castShadow = true; mesh.receiveShadow = true;
    (group || G.obj).add(mesh);
    return mesh;
  }
  function flat(geo) { var g = geo.toNonIndexed(); g.computeVertexNormals(); return g; }

  var O = F.objects;
  /* photovoltaic rack: 8 segments of 4 m, tilt 60 degrees, facing south */
  (function () {
    var pv = O.pv, tilt = pv.tilt * Math.PI / 180, L = pv.panel;
    var panelMat = lambert('#17355e'), frameMat = lambert('#c9ced2');
    pv.seg.forEach(function (s) {
      var g = sy(s.h);
      var board = new THREE.Mesh(new THREE.BoxGeometry(3.94, L, 0.08), panelMat);
      board.rotation.x = -(Math.PI / 2 - tilt);
      board.position.set(sx(s.x), g + pv.edge + (L / 2) * Math.sin(tilt), sz(s.y) - (L / 2) * Math.cos(tilt));
      board.castShadow = true; board.receiveShadow = true;
      G.obj.add(board);
      var hp = pv.edge + L * Math.sin(tilt);
      [-1.6, 1.6].forEach(function (dx) {
        var post = new THREE.Mesh(new THREE.BoxGeometry(0.12, hp, 0.12), frameMat);
        post.position.set(sx(s.x) + dx, g + hp / 2, sz(s.y) - L * Math.cos(tilt));
        post.castShadow = true;
        G.obj.add(post);
      });
    });
    var mid = pv.seg[4];
    addLabel('PV', mid.x - 2, mid.y, mid.h, 'obj', 'obj', 4.6);
  })();

  /* upper water tank */
  put(new THREE.Mesh(new THREE.CylinderGeometry(1.1, 1.1, 2, 20), lambert('#a9bfca')), O.w1.x, O.w1.y, O.w1.h, 1);
  addLabel('W1', O.w1.x, O.w1.y, O.w1.h, 'obj', 'obj', 3.4);

  /* polytunnel: half tube along the north-south axis */
  (function () {
    var t = O.t1, r = t.wid / 2, seg = 14, v = [], idx = [], i;
    for (i = 0; i <= seg; i++) { var a = Math.PI * i / seg, x = r * Math.cos(a), y = r * Math.sin(a); v.push(x, y, -t.len / 2, x, y, t.len / 2); }
    for (i = 0; i < seg; i++) { var k = 2 * i; idx.push(k, k + 1, k + 2, k + 1, k + 3, k + 2); }
    var g = new THREE.BufferGeometry();
    g.setAttribute('position', new THREE.Float32BufferAttribute(v, 3)); g.setIndex(idx); g.computeVertexNormals();
    var m = new THREE.Mesh(g, lambert('#f4f6ef', { transparent: true, opacity: 0.8, side: THREE.DoubleSide }));
    put(m, t.x, t.y, t.h, -0.15); m.receiveShadow = false;
    addLabel('T1', t.x, t.y, t.h, 'obj', 'obj', 3.4);
  })();

  /* livestock building with a gable roof, aviary */
  (function () {
    var b = O.b1, w = 10, d = 6, wall = 2.8, roofH = 1.6;
    put(new THREE.Mesh(new THREE.BoxGeometry(w, wall, d), lambert('#d9c7a3')), b.x, b.y, b.h, wall / 2 - 0.2);
    var x = w / 2 + 0.3, z = d / 2 + 0.3;
    var rg = new THREE.BufferGeometry();
    rg.setAttribute('position', new THREE.Float32BufferAttribute([-x, 0, -z, x, 0, -z, x, 0, z, -x, 0, z, -x, roofH, 0, x, roofH, 0], 3));
    rg.setIndex([0, 4, 5, 0, 5, 1, 3, 2, 5, 3, 5, 4, 0, 3, 4, 1, 5, 2]);
    put(new THREE.Mesh(flat(rg), lambert('#7a3b2e', { side: THREE.DoubleSide })), b.x, b.y, b.h, wall - 0.2);
    addLabel('B1', b.x, b.y, b.h, 'obj', 'obj', 6);
    var a = O.wol, box = new THREE.BoxGeometry(10, 2.5, 10);
    var faces = put(new THREE.Mesh(box, lambert('#f1d6b8', { transparent: true, opacity: 0.28, depthWrite: false })), a.x, a.y, a.h, 1.25);
    faces.castShadow = false; faces.receiveShadow = false;
    var edges = new THREE.LineSegments(new THREE.EdgesGeometry(box), new THREE.LineBasicMaterial({ color: col('#7a3b12') }));
    edges.position.copy(faces.position); G.obj.add(edges);
  })();

  /* earth cellar */
  (function () {
    var m1 = O.m1;
    var dome = new THREE.Mesh(new THREE.SphereGeometry(3.2, 18, 9, 0, Math.PI * 2, 0, Math.PI / 2), lambert('#6f8650'));
    dome.scale.set(1.15, 0.55, 1);
    put(dome, m1.x, m1.y, m1.h, -0.2);
    put(new THREE.Mesh(new THREE.BoxGeometry(0.4, 1.9, 1.3), lambert('#3a2a1c')), m1.x - 3.5, m1.y, ground(m1.x - 3.5, m1.y), 0.95);
    addLabel('M1', m1.x, m1.y, m1.h, 'obj', 'obj', 3.4);
  })();

  /* apiary: 3 hives and a hedge */
  (function () {
    var u = O.u1, colors = ['#e2b93b', '#3f6fb0', '#f0f0ea'];
    colors.forEach(function (cc, i) { put(new THREE.Mesh(new THREE.BoxGeometry(0.55, 0.7, 0.55), lambert(cc)), u.x + (i - 1) * 1.6, u.y, ground(u.x + (i - 1) * 1.6, u.y), 0.55); });
    put(new THREE.Mesh(new THREE.BoxGeometry(9, 2, 0.9), lambert('#3f7a3a')), u.x, u.y - 3.5, ground(u.x, u.y - 3.5), 1);
    addLabel('U1', u.x, u.y, u.h, 'obj', 'obj', 3.2);
  })();

  addLabel('K', O.k.x, O.k.y, O.k.top, 'obj', 'obj', 1.6);
  addLabel('Dom', O.dom.x, O.dom.y, O.dom.h, 'map', 'map', 8.5);

  /* planned orchard trees on terraces */
  (function () {
    var pts = F.orchard, N = pts.length;
    if (!N) return;
    var sph = new THREE.SphereGeometry(1, 9, 7), tr = new THREE.CylinderGeometry(0.12, 0.16, 1, 5); tr.translate(0, 0.5, 0);
    var crowns = new THREE.InstancedMesh(sph, new THREE.MeshLambertMaterial({ color: 0xffffff }), N);
    var trunks = new THREE.InstancedMesh(tr, lambert('#5b4632'), N);
    var d = new THREE.Object3D(), c = new THREE.Color(), a = col('#8fc46b'), b = col('#b9d87c');
    for (var i = 0; i < N; i++) {
      var g = sy(pts[i][2]);
      d.position.set(sx(pts[i][0]), g + 2.6, sz(pts[i][1])); d.scale.set(1.5, 1.4, 1.5); d.updateMatrix(); crowns.setMatrixAt(i, d.matrix);
      c.copy(a).lerp(b, ((i * 37) % 10) / 10); crowns.setColorAt(i, c);
      d.position.set(sx(pts[i][0]), g, sz(pts[i][1])); d.scale.set(1, 1.6, 1); d.updateMatrix(); trunks.setMatrixAt(i, d.matrix);
    }
    crowns.instanceColor.needsUpdate = true; crowns.castShadow = true; crowns.frustumCulled = false; trunks.frustumCulled = false;
    G.plan.add(crowns); G.plan.add(trunks);
  })();

  /* parcel boundaries as a low translucent ribbon */
  (function () {
    var mat = new THREE.MeshBasicMaterial({ color: 0xffe14d, transparent: true, opacity: 0.8, side: THREE.DoubleSide, depthWrite: false });
    Object.keys(F.parcels).forEach(function (k) {
      var ring = F.parcels[k], v = [], idx = [], count = 0;
      for (var i = 0; i < ring.length - 1; i++) {
        var a = ring[i], b = ring[i + 1], len = Math.hypot(b[0] - a[0], b[1] - a[1]), ns = Math.max(1, Math.ceil(len / 2));
        for (var s = 0; s <= ns; s++) {
          var t = s / ns, x = a[0] + (b[0] - a[0]) * t, y = a[1] + (b[1] - a[1]) * t, g = sy(ground(x, y));
          v.push(sx(x), g + 0.15, sz(y), sx(x), g + 1.5, sz(y));
          if (s > 0) { var q = 2 * (count - 1); idx.push(q, q + 1, q + 2, q + 1, q + 3, q + 2); }
          count++;
        }
      }
      var geo = new THREE.BufferGeometry();
      geo.setAttribute('position', new THREE.Float32BufferAttribute(v, 3)); geo.setIndex(idx);
      var mesh = new THREE.Mesh(geo, mat); mesh.renderOrder = 4;
      G.parcels.add(mesh);
    });
  })();

  /* zone, field and map labels */
  Object.keys(F.zones).forEach(function (k) {
    var z = F.zones[k];
    addLabel(k, z.label[0], z.label[1], ground(z.label[0], z.label[1]), 'zone', 'zone', k === 'S8a' || k === 'S8b' ? 17 : 2.2);
  });
  F.labels.forEach(function (L) { addLabel(L.t, L.x, L.y, L.h, L.c === 'water' ? 'water' : 'field', L.c === 'water' ? 'map' : 'field', 1.2); });

  /* scale bar 50 m and north arrow on the lake */
  (function () {
    var y = sy(M.lake) + 0.3;
    for (var i = 0; i < 5; i++) {
      var seg = new THREE.Mesh(new THREE.BoxGeometry(10, 0.3, 1.6), new THREE.MeshBasicMaterial({ color: i % 2 ? 0x111111 : 0xffffff }));
      seg.position.set(sx(262 + 10 * i), y, sz(16));
      root.add(seg);
    }
    addLabel('50 m', 282, 24, M.lake, 'map', 'map', 0.5);
    var arrow = new THREE.Mesh(new THREE.ConeGeometry(3, 9, 3), new THREE.MeshBasicMaterial({ color: 0xffffff }));
    arrow.rotation.x = -Math.PI / 2;
    arrow.position.set(sx(236), y + 0.5, sz(16));
    root.add(arrow);
    addLabel('N', 236, 27, M.lake, 'map', 'map', 0.5);
  })();

  /* ---------- sun ---------- */
  var state = { decl: -23.44, time: 12, shadows: true, vex: 1 };
  function sunAngles(decl, t) {
    var p = M.lat * Math.PI / 180, d = decl * Math.PI / 180, h = (t - 12) * 15 * Math.PI / 180;
    var el = Math.asin(Math.sin(p) * Math.sin(d) + Math.cos(p) * Math.cos(d) * Math.cos(h));
    var az = Math.atan2(Math.sin(h), Math.cos(h) * Math.sin(p) - Math.tan(d) * Math.cos(p));
    return { el: el * 180 / Math.PI, az: (180 + az * 180 / Math.PI + 360) % 360 };
  }
  function pl(x, digits) { return x.toFixed(digits).replace('.', ',').replace('-', '−'); }
  function updateSun() {
    var s = sunAngles(state.decl, state.time), el = s.el * Math.PI / 180, az = s.az * Math.PI / 180;
    var up = s.el > 0.3;
    var dir = new THREE.Vector3(Math.cos(el) * Math.sin(az), Math.max(Math.sin(el), 0.004), -Math.cos(el) * Math.cos(az));
    sun.position.copy(sun.target.position).addScaledVector(dir, 760);
    sun.intensity = up ? 0.75 : 0;
    hemi.intensity = up ? 0.78 : 0.42;
    var cast = up && state.shadows && state.vex === 1;
    shadowMesh.visible = cast;
    sun.castShadow = cast;
    $('sun-az').textContent = Math.round(s.az) + '°';
    $('sun-el').textContent = pl(s.el, 1) + '°';
    var hh = Math.floor(state.time), mm = Math.round((state.time - hh) * 60);
    $('sun-clock').textContent = (hh < 10 ? '0' : '') + hh + ':' + (mm < 10 ? '0' : '') + mm;
    $('sunwarn').hidden = up;
    shadowsDirty();
  }

  /* ---------- views ---------- */
  function setView(pos, target) {
    camera.position.set(pos[0], pos[1], pos[2]);
    controls.target.set(target[0], target[1], target[2]);
    controls.update();
    invalidate();
  }
  function k() { return camera.aspect < 0.9 ? 1.75 : (camera.aspect < 1.3 ? 1.25 : 1); }
  var pvMid = O.pv.seg[4];
  var views = {
    south: function () { var f = k(); setView([30 * f, 170 * f, 300 * f], [0, 6, -14]); },
    top: function () { var f = k(); setView([0, 480 * f, 0.6], [0, 0, 0]); },
    pv: function () { setView([sx(pvMid.x) + 16, sy(pvMid.h) + 24, sz(pvMid.y) + 66], [sx(pvMid.x) - 2, sy(pvMid.h) + 1, sz(pvMid.y) - 6]); },
    north: function () { var f = k(); setView([-50 * f, 170 * f, -310 * f], [0, 6, 10]); }
  };

  /* ---------- interface ---------- */
  function bindToggle(id, fn) { var el = $(id); el.addEventListener('change', function () { fn(el.checked); shadowsDirty(); }); }
  bindToggle('lyr-zones', function (v) { zonesMesh.visible = v; show.zone = v; });
  bindToggle('lyr-plan', function (v) { planMesh.visible = v; G.plan.visible = v; show.field = v; });
  bindToggle('lyr-obj', function (v) { G.obj.visible = v; show.obj = v; });
  bindToggle('lyr-labels', function (v) { show.all = v; });
  bindToggle('lyr-trees', function (v) { G.trees.visible = v; });
  bindToggle('lyr-s8a', function (v) { G.s8a.visible = v; });
  bindToggle('lyr-parcels', function (v) { G.parcels.visible = v; });
  bindToggle('lyr-shadow', function (v) { state.shadows = v; updateSun(); });
  bindToggle('vex', function (v) { state.vex = v ? 2 : 1; root.scale.y = state.vex; updateSun(); });

  var days = { 'day-dec': -23.44, 'day-mar': 0, 'day-jun': 23.44 };
  Object.keys(days).forEach(function (id) {
    $(id).addEventListener('click', function () {
      state.decl = days[id];
      Object.keys(days).forEach(function (o) { $(o).setAttribute('aria-pressed', o === id ? 'true' : 'false'); });
      updateSun();
    });
  });
  $('sun-time').addEventListener('input', function () { state.time = parseFloat(this.value); updateSun(); });
  ['south', 'top', 'pv', 'north'].forEach(function (v) { $('view-' + v).addEventListener('click', views[v]); });

  var toggleBtn = $('toggle-panel');
  toggleBtn.addEventListener('click', function () {
    var collapsed = app.classList.toggle('collapsed');
    toggleBtn.textContent = collapsed ? 'Pokaż panel' : 'Ukryj panel';
    toggleBtn.setAttribute('aria-expanded', collapsed ? 'false' : 'true');
  });

  (function () {
    var ul = $('zone-list');
    Object.keys(F.zones).forEach(function (code) {
      var z = F.zones[code], li = document.createElement('li');
      var sw = document.createElement('span'); sw.className = 'sw'; sw.style.background = z.color;
      var c = document.createElement('span'); c.className = 'code'; c.textContent = code;
      var nm = document.createElement('span'); nm.textContent = z.name;
      var ar = document.createElement('span'); ar.className = 'area'; ar.textContent = z.area.toLocaleString('pl-PL') + ' m²';
      li.appendChild(sw); li.appendChild(c); li.appendChild(nm); li.appendChild(ar);
      ul.appendChild(li);
    });
  })();

  /* tap on the terrain: coordinates, height, zone */
  function inRing(x, y, ring) {
    var inside = false;
    for (var i = 0, j = ring.length - 1; i < ring.length; j = i++) {
      var xi = ring[i][0], yi = ring[i][1], xj = ring[j][0], yj = ring[j][1];
      if (((yi > y) !== (yj > y)) && (x < (xj - xi) * (y - yi) / (yj - yi) + xi)) inside = !inside;
    }
    return inside;
  }
  function zoneAt(x, y) {
    var codes = Object.keys(F.zones);
    for (var i = 0; i < codes.length; i++) {
      var rings = F.zones[codes[i]].rings;
      for (var r = 0; r < rings.length; r++) if (inRing(x, y, rings[r])) return codes[i];
    }
    return null;
  }
  var ray = new THREE.Raycaster(), ptr = new THREE.Vector2(), down = null;
  canvas.addEventListener('pointerdown', function (e) { down = { x: e.clientX, y: e.clientY, t: Date.now() }; });
  canvas.addEventListener('pointerup', function (e) {
    if (!down || Math.hypot(e.clientX - down.x, e.clientY - down.y) > 6 || Date.now() - down.t > 600) { down = null; return; }
    down = null;
    var rect = canvas.getBoundingClientRect();
    ptr.set(((e.clientX - rect.left) / rect.width) * 2 - 1, -((e.clientY - rect.top) / rect.height) * 2 + 1);
    ray.setFromCamera(ptr, camera);
    var hit = ray.intersectObject(terrain, false)[0];
    if (!hit) return;
    var x = hit.point.x + HALF, y = HALF - hit.point.z, z = zoneAt(x, y);
    $('readout').textContent = 'E ' + Math.round(M.E0 + x).toLocaleString('pl-PL') + ' · N ' + Math.round(M.N0 + y).toLocaleString('pl-PL') +
      ' · ' + pl(ground(x, y), 1) + ' m n.p.m.' + (z ? ' · strefa ' + z + ': ' + F.zones[z].name : ' · poza gospodarstwem');
  });

  /* ---------- sizing and render loop ---------- */
  function resize() {
    var w = stage.clientWidth, h = stage.clientHeight;
    if (!w || !h) return;
    renderer.setSize(w, h, false);
    camera.aspect = w / h;
    camera.updateProjectionMatrix();
    invalidate();
  }
  if (window.ResizeObserver) new ResizeObserver(resize).observe(stage); else window.addEventListener('resize', resize);
  controls.addEventListener('change', invalidate);
  if (window.matchMedia) {
    var mq = window.matchMedia('(prefers-color-scheme: dark)');
    if (mq.addEventListener) mq.addEventListener('change', applyTheme); else if (mq.addListener) mq.addListener(applyTheme);
  }
  if (window.MutationObserver) new MutationObserver(applyTheme).observe(document.documentElement, { attributes: true, attributeFilter: ['data-theme'] });

  applyTheme();
  resize();
  views.south();
  updateSun();

  function frame() {
    requestAnimationFrame(frame);
    if (!dirty) return;
    dirty = false;
    renderer.render(scene, camera);
    placeLabels();
  }
  frame();
  window.__farm3d = { ready: true, views: views, invalidate: invalidate };
})();
