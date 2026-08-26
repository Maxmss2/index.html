package com.videocreator.app;

import android.app.Activity;
import android.os.Bundle;
import android.graphics.Color;
import android.view.Gravity;
import android.view.View;
import android.widget.*;

public class MainActivity extends Activity {
  LinearLayout queue;
  TextView status;
  @Override public void onCreate(Bundle savedInstanceState) {
    super.onCreate(savedInstanceState);
    LinearLayout root=new LinearLayout(this); root.setOrientation(LinearLayout.VERTICAL); root.setPadding(32,48,32,32); root.setBackgroundColor(Color.rgb(16,21,34));
    TextView title=new TextView(this); title.setText("🎬 VÍDEOCREATOR"); title.setTextColor(Color.WHITE); title.setTextSize(28); root.addView(title);
    TextView sub=new TextView(this); sub.setText("Central de agentes para criação de Shorts"); sub.setTextColor(Color.LTGRAY); root.addView(sub);
    final EditText command=new EditText(this); command.setHint("Ex.: Crie 3 Shorts sobre o espaço"); command.setTextColor(Color.WHITE); command.setHintTextColor(Color.LTGRAY); command.setSingleLine(false); root.addView(command,new LinearLayout.LayoutParams(-1,180));
    Button run=new Button(this); run.setText("🚀 EXECUTAR AGENTES"); root.addView(run);
    status=new TextView(this); status.setText("Pronto para testar. Motor em modo demonstração."); status.setTextColor(Color.rgb(184,192,208)); status.setPadding(0,16,0,16); root.addView(status);
    ScrollView scroll=new ScrollView(this); queue=new LinearLayout(this); queue.setOrientation(LinearLayout.VERTICAL); scroll.addView(queue); root.addView(scroll,new LinearLayout.LayoutParams(-1,0,1));
    run.setOnClickListener(v->{String c=command.getText().toString().trim(); if(c.isEmpty()){status.setText("Digite um comando primeiro.");return;} status.setText("🤖 Planejando sua produção..."); queue.removeAllViews(); for(int i=1;i<=3;i++){TextView item=new TextView(this); item.setText("🎬 Short "+i+"\n✍️ Roteiro preparado\n🟡 Aguardando motor online"); item.setTextColor(Color.WHITE); item.setTextSize(16); item.setPadding(20,20,20,20); queue.addView(item); View line=new View(this); line.setBackgroundColor(Color.DKGRAY); queue.addView(line,new LinearLayout.LayoutParams(-1,2));} status.setText("✅ 3 Shorts adicionados à fila de teste.");});
    setContentView(root);
  }
}
